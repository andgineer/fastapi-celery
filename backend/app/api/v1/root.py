from app import version
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def read_root() -> dict[str, str]:
    message = f"{version.VERSION}"
    return {"version": message}
