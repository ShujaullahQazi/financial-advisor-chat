"""
Configuration file for the FinAI Financial Advisor Agent
"""

# Agent Personality Configuration
AGENT_PERSONALITY = {
    "name": "FinAI",
    "version": "2.0",
    "traits": [
        "knowledgeable",
        "cautious", 
        "helpful",
        "ethical",
        "educational",
        "professional"
    ],
    "expertise": [
        "personal finance",
        "budgeting",
        "investment basics", 
        "retirement planning",
        "debt management",
        "emergency funds",
        "tax basics",
        "insurance fundamentals"
    ],
    "communication_style": "clear, professional, and educational",
    "risk_tolerance": "conservative",
    "disclaimer": "Always remind users to consult certified professionals for major financial decisions"
}

# Available Tools Configuration
AVAILABLE_TOOLS = {
    "compound_interest": {
        "name": "Compound Interest Calculator",
        "description": "Calculate compound interest growth over time",
        "keywords": ["compound interest", "interest rate", "investment growth", "savings growth"],
        "parameters": ["principal", "rate", "time", "compounds_per_year"]
    },
    "loan_payment": {
        "name": "Loan Payment Calculator", 
        "description": "Calculate monthly loan payments",
        "keywords": ["loan payment", "mortgage", "monthly payment", "loan calculator", "car loan"],
        "parameters": ["principal", "rate", "years"]
    },
    "retirement_savings": {
        "name": "Retirement Savings Calculator",
        "description": "Project retirement savings growth",
        "keywords": ["retirement", "401k", "savings", "retirement planning", "pension"],
        "parameters": ["monthly_contribution", "years", "annual_return", "current_savings"]
    },
    "emergency_fund": {
        "name": "Emergency Fund Calculator",
        "description": "Calculate recommended emergency fund size",
        "keywords": ["emergency fund", "emergency savings", "safety net"],
        "parameters": ["monthly_expenses", "months_coverage"]
    }
}

# Response Templates
RESPONSE_TEMPLATES = {
    "welcome": """
# 👋 Welcome to FinAI!

I'm your intelligent financial advisor agent, designed to help you make informed financial decisions.

## What I can help you with:

### 📊 **Financial Calculations**
- Compound interest and investment growth
- Loan payments and mortgage calculations  
- Retirement savings projections
- Emergency fund planning

### 📚 **Financial Education**
- Understanding financial concepts
- Budgeting strategies
- Investment basics
- Debt management

### 💡 **Financial Planning**
- Goal setting and tracking
- Risk assessment
- Portfolio diversification basics
- Tax-efficient strategies

## Getting Started
Try asking me questions like:
- "Calculate compound interest for $10,000 at 5% for 10 years"
- "What's a good emergency fund size for my situation?"
- "Help me understand 401(k) contributions"
- "How should I prioritize paying off debt vs saving?"

**Remember**: I provide educational guidance, but always consult certified professionals for major financial decisions.
""",
    
    "calculation_intro": "I'll help you with that calculation. Let me break down the results:",
    
    "disclaimer": """
> **Important**: This is educational information only. For personalized financial advice, please consult a certified financial advisor, accountant, or other qualified professional.
""",
    
    "error_message": "I apologize, but I encountered an error processing your request. Please try rephrasing your question or contact support if the issue persists."
}

# Session Configuration
SESSION_CONFIG = {
    "max_history_length": 50,
    "session_timeout_hours": 24,
    "auto_save_interval_minutes": 5,
    "default_preferences": {
        "risk_tolerance": "moderate",
        "investment_horizon": "long_term", 
        "financial_goals": [],
        "current_savings": 0,
        "monthly_income": 0,
        "monthly_expenses": 0
    }
}

# UI Configuration
UI_CONFIG = {
    "theme": {
        "primary_color": "#007bff",
        "secondary_color": "#6c757d", 
        "success_color": "#28a745",
        "warning_color": "#ffc107",
        "danger_color": "#dc3545",
        "background_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    },
    "features": {
        "typing_indicator": True,
        "markdown_rendering": True,
        "confidence_indicators": True,
        "tool_usage_indicators": True,
        "session_persistence": True
    }
}

# API Configuration
# Available Gemini 2.5 Models:
# - "gemini-2.5-flash-exp" (Fast, cost-effective, recommended for most use cases)
# - "gemini-2.5-pro-exp" (Most capable, slower, better for complex reasoning)
# - "gemini-2.0-flash-exp" (Fallback option if 2.5 not available)
API_CONFIG = {
    "model": "gemini-2.5-flash",  # Using Gemini 2.5 Flash
    "max_tokens": 2048,
    "temperature": 0.7,
    "timeout_seconds": 30,
    "retry_attempts": 3
}

# Security and Privacy
SECURITY_CONFIG = {
    "data_retention_days": 30,
    "encrypt_sensitive_data": True,
    "log_user_interactions": False,
    "anonymize_data": True
} 