from fastapi import APIRouter
from .chess import router as chess_router
from .queries import router as query_router

router = APIRouter()
router.include_router(chess_router, prefix="/chess", tags=["Chess"])
router.include_router(query_router, prefix="/queries", tags=["Queries"])