from fastapi import APIRouter
from app import modules_load
from pathlib import Path

router = APIRouter()

modules_load.asterisk(Path(__file__).parent, __package__, globals())
