from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class PredictionInput:
    model_key: str
    mileage: int
    engine_power: int
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool

    def to_record(self) -> dict:
        return asdict(self)
