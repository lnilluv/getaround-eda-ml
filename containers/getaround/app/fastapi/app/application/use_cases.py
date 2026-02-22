from app.application.ports import PredictionModelPort, UserReadPort
from app.domain.prediction import PredictionInput


class PredictRentalPriceUseCase:
    def __init__(self, predictor: PredictionModelPort) -> None:
        self._predictor = predictor

    def execute(self, features: PredictionInput) -> float:
        return self._predictor.predict(features)


class ListUsersUseCase:
    def __init__(self, users: UserReadPort) -> None:
        self._users = users

    async def execute(self) -> list[dict]:
        return await self._users.list_users()
