from typing import Dict

from app import version
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def read_root() -> Dict[str, str]:
    message = f"{version.VERSION}"
    return {"version": message}
