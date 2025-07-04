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

### Option 2: Railway

1. Connect your GitHub repository to Railway
2. Set the `GOOGLE_API_KEY` environment variable in Railway dashboard
3. Deploy automatically

### Option 3: Render

1. Connect your GitHub repository to Render
2. Set the `GOOGLE_API_KEY` environment variable
3. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn weather_agent:app --host=0.0.0.0 --port=$PORT`

### Option 4: DigitalOcean App Platform

1. Connect your GitHub repository
2. Set environment variables
3. Deploy with the provided configuration

## API Endpoints

- `GET /` - Serves the chat interface
- `POST /chat` - Chat endpoint that accepts chat history and returns AI response

## Environment Variables

- `GOOGLE_API_KEY`: Your Google Generative AI API key (required) 