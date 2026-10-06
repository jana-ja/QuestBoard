from fastapi import FastAPI

from quest_board.api.router import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Quest Board API",
    )

    app.include_router(api_router, prefix="/api")

    return app
