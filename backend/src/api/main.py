from fastapi import APIRouter
from .v1.textbook import router as textbook_router
from .v1.chat import router as chat_router
from .v1.labs import router as labs_router
from .v1.capstone import router as capstone_router

# Main API router
app = APIRouter()

# Include all API version 1 routes
app.include_router(textbook_router, prefix="/textbook", tags=["textbook"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(labs_router, prefix="/labs", tags=["labs"])
app.include_router(capstone_router, prefix="/capstone", tags=["capstone"])

__all__ = ["app"]