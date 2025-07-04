import uvicorn

if __name__ == "__main__":
    uvicorn.run("financial_advisor_chat:app", host="0.0.0.0", port=8000, reload=True) 