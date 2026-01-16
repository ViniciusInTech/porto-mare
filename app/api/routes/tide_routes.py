from fastapi import APIRouter, HTTPException
from app.api.schemas.tide_schemas import TideMessageResponse
from app.application.use_cases.generate_tide_message_use_case import GenerateTideMessageUseCase
from app.infrastructure.ai.openai_provider import OpenAIProvider
from app.infrastructure.location.api_location_provider import ApiLocationProvider
from app.infrastructure.location.cached_location_provider import CachedLocationProvider
from app.infrastructure.tide.tide_api_provider import TideApiProvider

router = APIRouter(prefix="/tide-message", tags=["tide"])

location_provider = CachedLocationProvider(ApiLocationProvider())

tide_provider = TideApiProvider()
open_ai = OpenAIProvider()

use_case = GenerateTideMessageUseCase(
    location_provider=location_provider,
    tide_provider=tide_provider,
    ai_provider=open_ai
)

@router.post(
    "",
    response_model=TideMessageResponse,
    summary="Get next tide change message",
    description=(
        "Returns information about the next tide change for a given port, "
        "including the expected time, tide level, tide type, and a short "
        "contextual message generated using artificial intelligence."
    ),
    responses={
        201: {
            "description": "Next tide change with AI-generated message"
        },
        404: {
            "description": "State or port not supported"
        }
    }
)
def get_tide_message(state: str, port_id: str):
    try:
        return use_case.execute(state, port_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
