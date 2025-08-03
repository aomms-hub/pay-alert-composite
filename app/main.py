import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.common_response import CommonResponse, CommonStatus
from app.constants.response import Responses
from app.routers import dashboard_route, notify_route
from config import CORS_ALLOW_ORIGINS

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

app = FastAPI()
app.include_router(dashboard_route.router)
app.include_router(notify_route.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return CommonResponse(
        status=CommonStatus.from_enum(Responses.SUCCESS),
        data="🚀 Pay Alert Composite is alive!"
    )
