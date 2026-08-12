from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api.routes import router, init_instances
from app.nats.nats_subscriber import NATSSubscriber

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

nats_subscriber = NATSSubscriber()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Functional Vision Assessment Backend")
    await nats_subscriber.connect()
    # Initialize route instances with connected NATS subscriber
    init_instances(nats_subscriber)
    yield
    logger.info("Shutting down Functional Vision Assessment Backend")
    await nats_subscriber.disconnect()

app = FastAPI(
    title="Functional Vision Assessment API",
    description="API for Functional Vision Assessment companion robot",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "functional-vision-assessment"}
