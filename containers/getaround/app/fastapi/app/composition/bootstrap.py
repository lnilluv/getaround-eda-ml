import logging

from fastapi import FastAPI

from app.adapters.http.routes import build_router
from app.adapters.mlflow.predictor import MlflowPredictor
from app.adapters.persistence.db import AsyncpgUserGateway
from app.application.use_cases import ListUsersUseCase, PredictRentalPriceUseCase
from app.composition.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app_description = """
This API exposes a health endpoint and a rental price prediction endpoint.
"""

app = FastAPI(
    title="Getaround API",
    description=app_description,
    version="1.0.0",
)

predictor = MlflowPredictor(model_uri=settings.model_uri)
predict_use_case = PredictRentalPriceUseCase(predictor=predictor)
users_gateway = AsyncpgUserGateway(db_url=settings.db_url)
users_use_case = ListUsersUseCase(users=users_gateway)

app.include_router(build_router(predict_use_case, users_use_case))


@app.on_event("startup")
async def startup() -> None:
    await users_gateway.connect()
    await users_gateway.create_schema()
    await users_gateway.seed_default_user()
    logger.info("Connected to the database")


@app.on_event("shutdown")
async def shutdown() -> None:
    await users_gateway.disconnect()
    logger.info("Disconnected from the database")
