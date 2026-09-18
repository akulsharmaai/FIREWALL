from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.services.ml_service import ml_model
from app.api.routes import health, analysis
from app.schemas.errors import ErrorResponse, ErrorDetail

# Initialize logging
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load ML model
    logger.info("Starting up Human Firewall Backend...")
    try:
        ml_model.load_model()
    except Exception as e:
        logger.error(f"Failed to load ML model: {e}")
        # Note: We don't crash the app here, it allows /health to report unloaded model
    yield
    # Shutdown
    logger.info("Shutting down...")

app = FastAPI(
    title="Human Firewall API",
    description="Backend API for the Human Firewall browser extension to detect manipulative patterns.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global validation exception handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc}")
    errors = exc.errors()
    msg = errors[0]["msg"] if errors else "Invalid request body."
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            success=False,
            error=ErrorDetail(code="VALIDATION_ERROR", message=msg)
        ).model_dump()
    )

# Include routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(health.router, prefix="/api/v1/health", tags=["Health"]) # Versioned alias
app.include_router(analysis.router, prefix="/api/v1", tags=["Analysis"])

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Human Firewall API is running. Check /docs for API documentation."}
