from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["API"])


@router.get("/")
async def api_root():
    return {
        "message": "Welcome to the ADE-APEX API",
        "version": "1.0.0",
    }


@router.get("/status")
async def status():
    return {
        "status": "ok",
        "service": "ADE-APEX",
        "version": "1.0.0",
    }
