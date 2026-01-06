"""
Financial Advisor Agent with personality and tool integration.
"""

import re
from typing import Dict, List, Optional

from ..config import AGENT_PERSONALITY, AVAILABLE_TOOLS
from .tools import FinancialTools


class FinancialAgent:
    """
    AI Financial Advisor Agent with configurable personality and tools.
    """

    def __init__(self):
        """Initialize the financial agent with tools and personality."""
        self.tools = FinancialTools()
        self.personality = AGENT_PERSONALITY

    def get_enhanced_context(self, session_data: Optional[Dict] = None) -> str:
        """
        Generate enhanced context for the AI model.

        Args:
            session_data: Optional session data for personalized context

        Returns:
            System prompt string with agent personality and context
        """
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
        """
        Detect if user is requesting a calculation.

        Args:
            message: User's message text

        Returns:
            Dictionary with tool info if calculation detected, None otherwise
        """
        message_lower = message.lower()

        for tool_id, tool_config in AVAILABLE_TOOLS.items():
            if any(keyword in message_lower for keyword in tool_config["keywords"]):
                return {"tool": tool_id, "description": tool_config["description"]}

        return None

    def extract_numbers(self, text: str) -> List[float]:
        """
        Extract numbers from text.

        Args:
            text: Text to extract numbers from

        Returns:
            List of extracted numbers as floats
        """
        numbers = re.findall(r"\d+\.?\d*", text)
        return [float(num) for num in numbers]

    def execute_tool(self, tool_name: str, numbers: List[float]) -> Optional[Dict]:
        """
        Execute the appropriate tool with extracted numbers.

        Args:
            tool_name: Name of the tool to execute
            numbers: List of numbers extracted from user message

        Returns:
            Tool result dictionary or None if execution failed
        """
        try:
            if tool_name == "compound_interest" and len(numbers) >= 3:
                return self.tools.calculate_compound_interest(numbers[0], numbers[1], numbers[2])
            elif tool_name == "loan_payment" and len(numbers) >= 3:
                return self.tools.calculate_loan_payment(numbers[0], numbers[1], int(numbers[2]))
            elif tool_name == "retirement_savings" and len(numbers) >= 3:
                current_savings = numbers[3] if len(numbers) > 3 else 0
                return self.tools.calculate_retirement_savings(
                    numbers[0], int(numbers[1]), numbers[2], current_savings
                )
            elif tool_name == "emergency_fund" and len(numbers) >= 1:
                months_coverage = numbers[1] if len(numbers) > 1 else 6
                return self.tools.calculate_emergency_fund(numbers[0], months_coverage)
        except Exception as e:
            return {"error": f"Calculation error: {str(e)}"}
        return None
