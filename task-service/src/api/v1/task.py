from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def get_health() -> dict:
    return {"message": "ok"}