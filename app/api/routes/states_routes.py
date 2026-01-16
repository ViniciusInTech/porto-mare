from fastapi import APIRouter
from app.application.use_cases.list_states_use_case import ListStatesUseCase
from app.domain.models.state import State
from app.infrastructure.location.api_location_provider import ApiLocationProvider
from app.infrastructure.location.cached_location_provider import CachedLocationProvider

router = APIRouter(prefix="/states", tags=["states"])

location_provider = CachedLocationProvider(ApiLocationProvider())

use_case = ListStatesUseCase(location_provider)

@router.get(
    "",
    response_model=list[State],
    summary="List supported states",
    description=(
        "Returns a list of Brazilian states supported by the tide API. "
        "Each state includes its code and display name, which can be used "
        "to query available ports and tide information."
    ),
    responses={
        200: {
            "description": "List of supported states"
        }
    }
)
def list_states():
    states = use_case.execute()
    return states

