from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get(
    "/hello-world",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
    summary="Hello World Endpoint",
    tags=["Example"],
)
def hello_world() -> dict[str, str]:
    """A simple hello world endpoint."""
    return JSONResponse({"message": "Hello, world!"})
