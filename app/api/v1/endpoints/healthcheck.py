from fastapi import APIRouter, status
from pydantic import BaseModel


class HealthcheckResponse(BaseModel):
    status: str
    message: str


router = APIRouter()


@router.get(
    "",
    response_model=HealthcheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Healthcheck endpoint",
    description="Check if the API is running",
)
async def healthcheck() -> HealthcheckResponse:
    return HealthcheckResponse(
        status="healthy",
        message="Service is running",
    )
