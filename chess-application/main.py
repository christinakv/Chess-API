from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from core.config import settings
from core.models.db_helper import db_helper
from core.models.base import Base
from api import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()

main_app = FastAPI(
    lifespan=lifespan
)

@main_app.get("/")
def root():
    return FileResponse("../ui/index.html")

main_app.include_router(
    api_router,
    prefix=settings.api.prefix,)

if __name__ == "__main__":
    uvicorn.run(
            "main:main_app",
                host = settings.run.host,
                port = settings.run.port,
                reload=True)