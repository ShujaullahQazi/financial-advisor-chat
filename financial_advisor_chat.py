# Import the necessary libraries
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai
import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import asyncio
import math
from agent_config import (
    AGENT_PERSONALITY, 
    AVAILABLE_TOOLS, 
    RESPONSE_TEMPLATES, 
    SESSION_CONFIG, 
    API_CONFIG
)

try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("API Key not found. Please set the GOOGLE_API_KEY environment variable.")
    exit()

# --- THE AGENT'S "BRAIN" ---
model = genai.GenerativeModel(API_CONFIG["model"])

app = FastAPI()

# In-memory storage for sessions (in production, use a database)
sessions: Dict[str, Dict] = {}

class ChatRequest(BaseModel):
    history: List[str]
    session_id: Optional[str] = None
    user_preferences: Optional[Dict] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    tools_used: List[str] = []
    confidence: float

class SessionData(BaseModel):
    user_id: str
    created_at: datetime
    preferences: Dict
    conversation_history: List[Dict]
    financial_profile: Dict

# Agent Tools
class FinancialTools:
    @staticmethod
    def calculate_compound_interest(principal: float, rate: float, time: float, compounds_per_year: int = 12):
        """Calculate compound interest"""
        amount = principal * (1 + rate/compounds_per_year)**(compounds_per_year * time)
        return {
            "final_amount": round(amount, 2),
            "interest_earned": round(amount - principal, 2),
            "formula": f"A = P(1 + r/n)^(nt) = {principal}(1 + {rate}/{compounds_per_year})^({compounds_per_year * time})"
        }
    
    @staticmethod
    def calculate_loan_payment(principal: float, rate: float, years: int):
        """Calculate monthly loan payment"""
        monthly_rate = rate / 12 / 100
        num_payments = years * 12
        if monthly_rate == 0:
            monthly_payment = principal / num_payments
        else:
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        return {
            "monthly_payment": round(monthly_payment, 2),
            "total_payment": round(monthly_payment * num_payments, 2),
            "total_interest": round(monthly_payment * num_payments - principal, 2)
        }
    
    @staticmethod
    def calculate_retirement_savings(monthly_contribution: float, years: int, annual_return: float, current_savings: float = 0):
        """Calculate retirement savings projection"""
        monthly_return = annual_return / 12 / 100
        num_months = years * 12
        
        if monthly_return == 0:
            total_savings = current_savings + (monthly_contribution * num_months)
        else:
            total_savings = current_savings * (1 + monthly_return)**num_months + \
                          monthly_contribution * ((1 + monthly_return)**num_months - 1) / monthly_return
        
        return {
            "total_savings": round(total_savings, 2),
            "contributions": round(monthly_contribution * num_months, 2),
            "interest_earned": round(total_savings - (current_savings + monthly_contribution * num_months), 2)
        }
    
    @staticmethod
    def calculate_emergency_fund(monthly_expenses: float, months_coverage: float = 6):
        """Calculate recommended emergency fund size"""
        recommended_amount = monthly_expenses * months_coverage
        return {
            "recommended_amount": round(recommended_amount, 2),
            "monthly_expenses": monthly_expenses,
            "months_coverage": months_coverage,
            "explanation": f"Emergency fund should cover {months_coverage} months of expenses"
        }

# Enhanced Agent with Memory and Tools
class FinancialAgent:
    def __init__(self):
        self.tools = FinancialTools()
        self.personality = AGENT_PERSONALITY
    
    def get_enhanced_context(self, session_data: Optional[Dict] = None) -> str:
        """Generate enhanced context for the agent"""
        base_context = f"""
You are {self.personality['name']}, an AI financial advisor with the following characteristics:
- Personality: {', '.join(self.personality['traits'])}
- Expertise: {', '.join(self.personality['expertise'])}
- Communication: {self.personality['communication_style']}

IMPORTANT GUIDELINES:
1. Always format responses using Markdown for clarity
2. Use headings, bullet points, and bold text for better readability
3. Provide educational explanations, not just answers
4. Always remind users to consult certified professionals for major decisions
5. Be conservative and risk-aware in your advice
6. Ask clarifying questions when needed
7. Use available tools for calculations when relevant

AVAILABLE TOOLS:
- Compound interest calculator
- Loan payment calculator  
- Retirement savings calculator

When users ask for calculations, use the appropriate tool and explain the results.
"""
        
        if session_data:
            user_context = f"""
USER CONTEXT:
- Session ID: {session_data.get('session_id', 'Unknown')}
- Previous interactions: {len(session_data.get('conversation_history', []))}
- User preferences: {session_data.get('preferences', {})}
- Financial profile: {session_data.get('financial_profile', {})}
"""
            base_context += user_context
        
        return base_context
    
    def detect_calculation_request(self, message: str) -> Optional[Dict]:
        """Detect if user is requesting a calculation"""
        message_lower = message.lower()
        
        # Check each tool's keywords
        for tool_id, tool_config in AVAILABLE_TOOLS.items():
            if any(keyword in message_lower for keyword in tool_config["keywords"]):
                return {"tool": tool_id, "description": tool_config["description"]}
        
        return None
    
    def extract_numbers(self, text: str) -> List[float]:
        """Extract numbers from text"""
        import re
        numbers = re.findall(r'\d+\.?\d*', text)
        return [float(num) for num in numbers]
    
    def execute_tool(self, tool_name: str, numbers: List[float]) -> Optional[Dict]:
        """Execute the appropriate tool with extracted numbers"""
        try:
            if tool_name == "compound_interest" and len(numbers) >= 3:
                return self.tools.calculate_compound_interest(numbers[0], numbers[1], numbers[2])
            elif tool_name == "loan_payment" and len(numbers) >= 3:
                return self.tools.calculate_loan_payment(numbers[0], numbers[1], int(numbers[2]))
            elif tool_name == "retirement_savings" and len(numbers) >= 3:
                current_savings = numbers[3] if len(numbers) > 3 else 0
                return self.tools.calculate_retirement_savings(numbers[0], int(numbers[1]), numbers[2], current_savings)
            elif tool_name == "emergency_fund" and len(numbers) >= 1:
                months_coverage = numbers[1] if len(numbers) > 1 else 6
                return self.tools.calculate_emergency_fund(numbers[0], months_coverage)
        except Exception as e:
            return {"error": f"Calculation error: {str(e)}"}
        return None

# Initialize the agent
agent = FinancialAgent()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Get or create session
        session_id = request.session_id or str(uuid.uuid4())
        if session_id not in sessions:
            sessions[session_id] = {
                "session_id": session_id,
                "created_at": datetime.now(),
                "conversation_history": [],
                "preferences": request.user_preferences or {},
                "financial_profile": {}
            }
        
        session_data = sessions[session_id]
        
        # Get the latest user message
        latest_message = request.history[-1] if request.history else ""
        
        # Check for calculation requests
        calculation_request = agent.detect_calculation_request(latest_message)
        tools_used = []
        calculation_result = None
        
        if calculation_request:
            numbers = agent.extract_numbers(latest_message)
            if numbers:
                calculation_result = agent.execute_tool(calculation_request["tool"], numbers)
                tools_used.append(calculation_request["description"])
        
        # Build enhanced prompt
        context = agent.get_enhanced_context(session_data)
        
        # Add calculation results to context if available
        if calculation_result and "error" not in calculation_result:
            context += f"\n\nCALCULATION RESULT:\n{json.dumps(calculation_result, indent=2)}\n\nPlease explain these results to the user in a clear, educational manner."
        
        # Combine context with conversation history
        full_prompt = context + "\n\nCONVERSATION HISTORY:\n" + "\n".join(request.history)
        
        # Generate response
        response = model.generate_content(full_prompt)
        response_text = response.text
        
        # Update session
        session_data["conversation_history"].append({
            "timestamp": datetime.now().isoformat(),
            "user_message": latest_message,
            "ai_response": response_text,
            "tools_used": tools_used
        })
        
        # Calculate confidence (simplified - in production, use more sophisticated methods)
        confidence = 0.9 if calculation_result else 0.8
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            tools_used=tools_used,
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get session information"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    if session_id in sessions:
        del sessions[session_id]
    return {"message": "Session deleted"}

@app.get("/")
def root():
    return FileResponse("chat.html")

# WebSocket support for real-time chat
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process message similar to HTTP endpoint
            # (Implementation would be similar to the /chat endpoint)
            
            response = {
                "type": "message",
                "content": "WebSocket response",
                "session_id": session_id
            }
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for session {session_id}")
