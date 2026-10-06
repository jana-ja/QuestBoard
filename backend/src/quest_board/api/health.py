from fastapi import APIRouter

from quest_board.schemas.health import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")  # response_model is redundant here because of return type annotation
async def check_health() -> HealthResponse:
    return HealthResponse(status="ok")
