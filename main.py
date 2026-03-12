import os
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional

# Pydantic models for response validation
class SecretsCheckResponse(BaseModel):
    is_openai_key_present: bool
    is_calendar_token_present: bool
    
class HelloResponse(BaseModel):
    message: str

# Initialize FastAPI app
app = FastAPI(
    title="Cloud Run Secrets API",
    description="API to check environment variables in Cloud Run",
    version="1.0.0"
)

@app.get("/", response_model=HelloResponse)
async def read_root():
    """Root endpoint to verify service is running."""
    return HelloResponse(message="Hello World from Cloud Run!")

@app.get("/my-secrets")
async def read_secrets(
):
    """
    Check status of required secrets.
    Only accessible by admin users.
    """
    try:
        openai_key = os.getenv("OPENAI_API_KEY", "Not Found")
        calendar_token = os.getenv("GOOGLE_CALENDAR_TOKEN", "Not Found")

        return {
            "openai_key": openai_key,
            "calendar_token": calendar_token
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error checking secrets: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
