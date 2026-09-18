from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.schemas.errors import ErrorResponse, ErrorDetail
from app.services.analysis_service import analyze_content
from app.core.logging import logger

router = APIRouter()

@router.post(
    "/analyze", 
    response_model=AnalysisResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    summary="Analyze content for manipulation"
)
async def analyze(request: AnalysisRequest):
    try:
        if not request.text or not request.text.strip():
            logger.warning("Received empty text for analysis.")
            return JSONResponse(
                status_code=400,
                content=ErrorResponse(
                    success=False,
                    error=ErrorDetail(code="INVALID_INPUT", message="Text cannot be empty.")
                ).model_dump()
            )
            
        result = analyze_content(request)
        return result
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                success=False,
                error=ErrorDetail(code="INTERNAL_ERROR", message="An unexpected error occurred during analysis.")
            ).model_dump()
        )
