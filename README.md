# 🤖 FinAI - Financial Advisor AI Agent

A sophisticated AI-powered financial advisor agent built with FastAPI and Google's Gemini AI. FinAI provides intelligent financial guidance, calculations, and educational content while maintaining ethical boundaries.

## ✨ Features

### 🧠 **Intelligent Agent Capabilities**
- **Memory & Context**: Remembers conversation history and user preferences
- **Session Management**: Persistent sessions with user data
- **Personality**: Configurable agent personality and communication style
- **Tool Integration**: Built-in financial calculators and analysis tools

### 📊 **Financial Tools**
- **Compound Interest Calculator**: Investment growth projections
- **Loan Payment Calculator**: Mortgage and loan payment calculations
- **Retirement Savings Calculator**: 401(k) and retirement planning
- **Emergency Fund Calculator**: Recommended emergency fund sizing

### 🎨 **Enhanced User Experience**
- **Modern UI**: Beautiful, responsive design with gradient backgrounds
- **Markdown Rendering**: Rich text formatting for better readability
- **Typing Indicators**: Real-time feedback during AI processing
- **Confidence Indicators**: Shows AI confidence levels
- **Tool Usage Tracking**: Displays which tools were used in responses

### 🔧 **Technical Features**
- **WebSocket Support**: Real-time communication capabilities
- **Session Persistence**: Local storage for conversation continuity
- **Error Handling**: Graceful error management and user feedback
- **Configuration System**: Easily customizable agent behavior

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google AI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd genai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export GOOGLE_API_KEY="your-google-ai-api-key"
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8000`

## 🛠️ Configuration

The agent is highly configurable through `agent_config.py`:

### Agent Personality
```python
AGENT_PERSONALITY = {
    "name": "FinAI",
    "traits": ["knowledgeable", "cautious", "helpful", "ethical"],
    "expertise": ["personal finance", "budgeting", "investment basics"],
    "communication_style": "clear, professional, and educational"
}
```

### Available Tools
```python
AVAILABLE_TOOLS = {
    "compound_interest": {
        "name": "Compound Interest Calculator",
        "keywords": ["compound interest", "interest rate", "investment growth"],
        "parameters": ["principal", "rate", "time", "compounds_per_year"]
    }
    # ... more tools
}
```

## 📝 Usage Examples

### Financial Calculations
- "Calculate compound interest for $10,000 at 5% for 10 years"
- "What would my monthly mortgage payment be for $300,000 at 4% for 30 years?"
- "How much will I have in retirement if I save $500/month for 30 years at 7% return?"

### Financial Education
- "What's a good emergency fund size?"
- "Help me understand 401(k) contributions"
- "How should I prioritize paying off debt vs saving?"

### Financial Planning
- "What's the 50/30/20 budgeting rule?"
- "How do I start investing as a beginner?"
- "What are the benefits of a Roth IRA?"

## 🔒 Security & Privacy

- **Data Retention**: Sessions are stored in memory (configurable for production)
- **No Sensitive Data**: Agent doesn't store personal financial information
- **Educational Focus**: Provides guidance, not specific investment advice
- **Professional Disclaimers**: Always reminds users to consult professionals

## 🏗️ Architecture

```
genai/
├── financial_advisor_chat.py  # Main FastAPI application
├── agent_config.py           # Configuration and settings
├── chat.html                 # Frontend interface
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

### Key Components

1. **FinancialAgent Class**: Core agent logic with personality and tools
2. **FinancialTools Class**: Mathematical calculations and analysis
3. **Session Management**: User session tracking and persistence
4. **WebSocket Support**: Real-time communication infrastructure
5. **Configuration System**: Centralized settings management

## 🔧 API Endpoints

- `GET /`: Main chat interface
- `POST /chat`: Send messages and receive AI responses
- `GET /session/{session_id}`: Retrieve session information
- `DELETE /session/{session_id}`: Delete a session
- `WS /ws/{session_id}`: WebSocket endpoint for real-time chat

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
1. Set up environment variables
2. Use a production WSGI server (Gunicorn, uvicorn)
3. Configure reverse proxy (Nginx)
4. Set up SSL certificates

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

**Important**: This AI agent provides educational financial information only. It does not provide investment, legal, or tax advice. Always consult with qualified professionals for personalized financial advice and major financial decisions.

## 🆘 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the documentation
- Review the configuration options

---

**Built with ❤️ using FastAPI, Google Gemini AI, and modern web technologies** 