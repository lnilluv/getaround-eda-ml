from typing import Protocol

from app.domain.prediction import PredictionInput


class PredictionModelPort(Protocol):
    def predict(self, features: PredictionInput) -> float:
        ...


class UserReadPort(Protocol):
    async def list_users(self) -> list[dict]:
        ...
