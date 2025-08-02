import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.client.db_client import database
from app.models.common_response import CommonResponse, CommonStatus
from app.constants.response import Responses
from app.consumer.rabbit_consumer import RabbitClient
from app.routers import consumer_route, dashboard_route
from config import CORS_ALLOW_ORIGINS

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

rabbit_client = RabbitClient()
is_sleeping = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting app...")
    await database.connect()
    await rabbit_client.start()
    yield
    logging.info("Shutting down app...")
    await database.disconnect()
    await rabbit_client.close()

app = FastAPI(lifespan=lifespan)
app.include_router(consumer_route.router)
app.include_router(dashboard_route.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,       # หรือ ["*"] ถ้าอยากเปิดหมด
    allow_credentials=True,      # อนุญาตส่ง cookie
    allow_methods=["*"],         # อนุญาตทุก HTTP method (GET, POST, PUT, DELETE)
    allow_headers=["*"],         # อนุญาตทุก header
)

@app.get("/")
async def root():
    return CommonResponse(
        status=CommonStatus.from_enum(Responses.SUCCESS),
        data="🚀 Pay Alert Composite is alive!"
    )

@app.post("/service/sleep")
async def sleep_service():
    global is_sleeping
    await database.disconnect()
    is_sleeping = True
    return {"status": "service sleeping"}

@app.get("/service/status")
async def get_status():
    return {"sleeping": is_sleeping}