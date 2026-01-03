from fastapi import FastAPI
from app.api.v1 import auth

app = FastAPI(title="Teacher Assistance Platform API")

# Include the Auth Router
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "TAP API is running"}