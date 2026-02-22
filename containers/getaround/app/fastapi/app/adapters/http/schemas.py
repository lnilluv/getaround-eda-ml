from pydantic import BaseModel

from app.domain.prediction import PredictionInput


class PredictionFeaturesDTO(BaseModel):
    model_key: str = "Citroen"
    mileage: int = 150000
    engine_power: int = 100
    fuel: str = "diesel"
    paint_color: str = "green"
    car_type: str = "convertible"
    private_parking_available: bool = True
    has_gps: bool = True
    has_air_conditioning: bool = True
    automatic_car: bool = True
    has_getaround_connect: bool = True
    has_speed_regulator: bool = True
    winter_tires: bool = True

    def to_domain(self) -> PredictionInput:
        return PredictionInput(**self.model_dump())
