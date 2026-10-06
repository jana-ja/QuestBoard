from fastapi import APIRouter

from quest_board.api.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router)
