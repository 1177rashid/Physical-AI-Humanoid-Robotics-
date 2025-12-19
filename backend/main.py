from fastapi import FastAPI
from src.api.main import app as api_router

app = FastAPI(title="AI-Native Textbook API", version="1.0.0")

# Include API routes
app.include_router(api_router, prefix="/v1")

@app.get("/")
def read_root():
    return {"message": "AI-Native Textbook API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)