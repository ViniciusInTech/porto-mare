from fastapi import APIRouter, HTTPException

from app.application.use_cases.list_ports_use_case import ListPortsUseCase
from app.domain.models.port import Port
from app.infrastructure.location.api_location_provider import ApiLocationProvider
from app.infrastructure.location.cached_location_provider import CachedLocationProvider

router = APIRouter(prefix="/states/{state_code}/ports", tags=["ports"])

location_provider = CachedLocationProvider(ApiLocationProvider())

use_case = ListPortsUseCase(location_provider=location_provider)

@router.get(
    "",
    response_model=list[Port],
    summary="List ports by state",
    description=(
        "Returns a list of ports available for a given Brazilian state. "
        "The state code must be a valid two-letter lowercase abbreviation "
        "supported by the tide API (e.g. `pe`, `pb`, `al`)."
    ),
    responses={
        200: {
            "description": "List of ports for the given state"
        },
        404: {
            "description": "State not supported"
        }
    }
)
def list_ports(state_code: str):
    try:
        return use_case.execute(state_code)
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="State not supported"
        )
