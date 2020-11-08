from pathlib import Path

from app import modules_load
from fastapi import APIRouter

router = APIRouter()

modules_load.asterisk(Path(__file__).parent, __package__, globals())
