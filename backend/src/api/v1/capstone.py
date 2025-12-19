from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_capstone_info():
    return {"message": "Capstone API endpoint"}