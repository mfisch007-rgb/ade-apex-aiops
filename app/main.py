from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.v1 import router as api_router
from app.core import configure_logging
from app.config.settings import settings
from app.kernel.runtime import kernel

configure_logging(settings.LOG_LEVEL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    ADE-APEX application lifecycle.
    """
    await kernel.start()
    yield
    await kernel.stop()


app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise AI Operating System",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/", tags=["System"])
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "kernel": kernel.status(),
    }


@app.get("/health", tags=["System"])
async def health():
    return JSONResponse(
        {
            "status": "healthy",
            "service": settings.APP_NAME,
            "kernel": kernel.status(),
        }
    )
