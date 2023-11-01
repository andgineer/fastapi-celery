from app.api.v1.auth import router as auth_router
from app.api.v1.root import router as root_router
from app.api.v1.words import router as words_router
from fastapi import APIRouter

TAGS = [
    {
        "name": "tests",
        "description": "Requests to test the service health.",
    },
    {
        "name": "security",
        "description": "JWT auth",
        "externalDocs": {
            "description": "JWT auth summary",
            "url": "https://example.com",
        },
    },
]

ROUTE_TABLE = [
    dict(router=root_router, tag="tests"),
    dict(prefix="/auth", router=auth_router, tag="security"),
    dict(prefix="/words", router=words_router, tag="words"),
]


router = APIRouter()
for route in ROUTE_TABLE:
    if "prefix" in route:
        router.include_router(
            route["router"], tags=[route["tag"]], prefix=route["prefix"]
        )
    else:
        router.include_router(route["router"], tags=[route["tag"]])
