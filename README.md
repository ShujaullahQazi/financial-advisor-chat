# Financial Advisor Chat Agent

A FastAPI-based chat application that provides financial advice using Google's Gemini AI.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your Google API key as an environment variable:
```bash
# Windows
set GOOGLE_API_KEY=your_api_key_here

# Linux/Mac
export GOOGLE_API_KEY=your_api_key_here
```

3. Run locally:
```bash
python run.py
```

The application will be available at `http://localhost:8000`

## Deployment Options

### Option 1: Heroku (Recommended for beginners)

1. Install Heroku CLI and login
2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Set your API key in Heroku:
```bash
heroku config:set GOOGLE_API_KEY=your_api_key_here
```

4. Deploy:
```bash
git add .
git commit -m "Initial deployment"
git push heroku main
```


### Render

1. Connect your GitHub repository to Render
2. Set the `GOOGLE_API_KEY` environment variable
3. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn financial_advisor_chat:app --host=0.0.0.0 --port=$PORT`
4. **Alternative**: Use the `render.yaml` file for automatic configuration


## API Endpoints

- `GET /` - Serves the chat interface
- `POST /chat` - Chat endpoint that accepts chat history and returns AI response

## Environment Variables

- `GOOGLE_API_KEY`: Your Google Generative AI API key (required) 
