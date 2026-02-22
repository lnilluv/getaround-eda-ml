## Context 

Video of project: https://youtu.be/QUoh_RfaAc8

Getaround is a service where drivers rent cars from owners for a specific time period, from an hour to a few days long. 

When renting a car, clients have to complete a checkin flow at the beginning of the rental and a checkout flow at the end of the rental in order to:
- assess the state of the car and notify other parties of pre-existing damages or damages that occurred during the rental,
- compare fuel levels,
- measure how many kilometers were driven.

The checkin and checkout of the rentals can be done with two major flows:
- Mobile rental agreement on native apps: driver and owner meet and both sign the rental agreement on the owner’s smartphone
- Connect: the driver doesn’t meet the owner and opens the car with his smartphone
(The third possibility, paper contract, is negligible).

At the end of the rental, drivers are supposed to bring back the car on time, but it happens from time to time that they are late for the checkout.

Late returns at checkout can generate high friction for the next driver if the car was supposed to be rented again on the same day : Customer service often reports users unsatisfied because they had to wait for the car to come back from the previous rental or users that even had to cancel their rental because the car wasn’t returned on time.

In order to mitigate those issues it was decided to implement a minimum delta between two rentals. A car won’t be displayed in the search results if the requested checkin or checkout times are too close from an already booked rental.

It solves the late checkout issue but also potentially hurts Getaround/owners revenues: we need to find the right trade off.

The product management team still needs to decide:
- threshold: how long should the minimum delay be?
- scope: should the feature be enabled for all cars?, only Connect cars?



## Goals of the project
 - Create a web dashboard that will help the product management team to answer the above questions
 - Create a documented online API to suggest optimum car rental price per day for car owners using Machine Learning


## Project structure

- `containers/getaround/`: production Docker stack for VPS deployment (Traefik, FastAPI, PostgreSQL, MLflow, MinIO, Streamlit).
- `containers/getaround/app/fastapi/app/`: API codebase structured with hexagonal boundaries (`domain`, `application`, `adapters`, `composition`).
- `streamlit_dev/`: standalone local Streamlit environment.
- `data/`: source datasets.
- `ml_models/`: model experiments.
- `model_final.py`: current model training/logging script.

## VPS deployment quickstart

1. Copy `containers/getaround/.env.example` to `containers/getaround/.env`.
2. Replace every `change-me` value with strong secrets.
3. Set DNS records for the hostnames used in `.env`.
4. Run:

```bash
cd containers/getaround
docker compose build
docker compose up -d
```

Security notes:
- Traefik insecure dashboard mode is disabled.
- MinIO bucket is created without anonymous download policy.
- Secrets are injected with environment variables and must not be committed.

## Deliverables

- Web Dashboard: [https://streamlit.pryda.dev](https://streamlit.pryda.dev)

- MLFlow Server: [https://mlflow.pryda.dev](https://mlflow.pryda.dev)

- Documented online API for price prediction: [https://api.pryda.dev/docs](https://api.pryda.dev/docs)

You can test the API by running the following code in python:

````python

import requests

payload = {
    "model_key": "Citroën",
    "mileage": 150411,
    "engine_power": 100,
    "fuel": "diesel",
    "paint_color": "green",
    "car_type": "convertible",
    "private_parking_available": True,
    "has_gps": True,
    "has_air_conditioning": True,
    "automatic_car": True,
    "has_getaround_connect": True,
    "has_speed_regulator": True,
    "winter_tires": True
}

r = requests.post(
    "https://api.pryda.dev/predict", json=payload)
print(r.json())


````
Or by running the following command in your terminal:

````bash

curl -X 'POST' \
  'https://api.pryda.dev/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "model_key": "Citroën",
  "mileage": 150000,
  "engine_power": 100,
  "fuel": "diesel",
  "paint_color": "green",
  "car_type": "convertible",
  "private_parking_available": true,
  "has_gps": true,
  "has_air_conditioning": true,
  "automatic_car": true,
  "has_getaround_connect": true,
  "has_speed_regulator": true,
  "winter_tires": true
}'
````
