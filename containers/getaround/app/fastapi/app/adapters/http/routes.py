import logging

from fastapi import APIRouter, HTTPException

from app.adapters.http.schemas import PredictionFeaturesDTO
from app.application.use_cases import ListUsersUseCase, PredictRentalPriceUseCase

logger = logging.getLogger(__name__)


def build_router(
    predict_use_case: PredictRentalPriceUseCase,
    users_use_case: ListUsersUseCase,
) -> APIRouter:
    router = APIRouter()

    @router.get("/", tags=["Default"])
    async def read_root() -> list[dict]:
        return await users_use_case.execute()

    @router.post("/prediction", tags=["Rental price prediction"])
    async def predict(features: PredictionFeaturesDTO) -> dict:
        try:
            prediction = predict_use_case.execute(features.to_domain())
            return {"prediction": prediction}
        except Exception as exc:
            logger.exception("Prediction failed: %s", exc)
            raise HTTPException(status_code=500, detail="Internal Server Error") from exc

    return router
