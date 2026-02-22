import mlflow
import pandas as pd

from app.domain.prediction import PredictionInput


class MlflowPredictor:
    def __init__(self, model_uri: str) -> None:
        self._model_uri = model_uri
        self._loaded_model = None

    def _ensure_model(self):
        if self._loaded_model is None:
            self._loaded_model = mlflow.pyfunc.load_model(self._model_uri)
        return self._loaded_model

    def predict(self, features: PredictionInput) -> float:
        features_df = pd.DataFrame(features.to_record(), index=[0])
        prediction = self._ensure_model().predict(features_df)
        return float(prediction.tolist()[0])
