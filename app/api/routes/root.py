from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root() -> dict[str, str]:
    return {
        "service": "nexus-platform",
        "message": "Nexus Platform is running",
    }