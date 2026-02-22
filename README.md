# Getaround Data Platform: Analytics + ML API + Production Deployment

Video walkthrough: https://youtu.be/QUoh_RfaAc8

This project reproduces a realistic product-data use case end to end: data analysis for rental delay policy, machine-learning pricing inference, and production deployment on a VPS with a containerized multi-service stack.

## Problem statement

Getaround rentals can be late at checkout. Late returns create downstream friction for the next renter and can lead to cancellations. The product team needs to choose:

- the minimum time delta threshold between rentals,
- the feature scope (all cars vs Connect-only),
- the operational tradeoff between customer experience and utilization/revenue.

## What this repository delivers

- An interactive analytics dashboard to evaluate delay behavior and policy thresholds.
- A production FastAPI service exposing a rental price prediction endpoint.
- MLflow tracking + artifact storage for model lifecycle management.
- A VPS-ready Docker Compose platform with routing, persistence, and hardened defaults.

## Live services

- Dashboard: [https://streamlit.pryda.dev](https://streamlit.pryda.dev)
- MLflow: [https://mlflow.pryda.dev](https://mlflow.pryda.dev)
- API docs: [https://api.pryda.dev/docs](https://api.pryda.dev/docs)

## Technical scope and complexity

This is not only an EDA notebook project. It includes:

- Data analysis workflow for threshold decision-making and cancellation-risk interpretation.
- ML training and model logging workflow.
- API serving architecture using hexagonal boundaries in FastAPI (`domain`, `application`, `adapters`, `composition`).
- Container orchestration across routing, backend, dashboard, model tracking, database, and object storage services.
- Security hardening and dependency remediation for deployment readiness.

## Architecture overview

Runtime topology:

```text
Internet
  -> Traefik (TLS + routing)
      -> FastAPI service (pricing inference)
      -> Streamlit dashboard (analytics)
      -> MLflow tracking server

FastAPI -> PostgreSQL
MLflow  -> SQLite backend store + MinIO artifacts
```

FastAPI internal structure:

```text
adapters -> application -> domain
         \-> composition root (wiring)
```

## Stack

| Layer | Technologies |
|---|---|
| Data and analysis | pandas, numpy, plotly, matplotlib, seaborn |
| ML and model lifecycle | scikit-learn, xgboost, MLflow |
| API | FastAPI, uvicorn, pydantic |
| Dashboard | Streamlit |
| Data stores | PostgreSQL, SQLite (MLflow metadata), MinIO |
| Platform and routing | Docker, Docker Compose, Traefik |
| Security and quality checks | Safety/pip-audit workflow, dependency pinning, hardened container defaults |

## Repository layout

- `containers/getaround/`: production deployment stack.
- `containers/getaround/app/fastapi/app/`: FastAPI service code with hexagonal structure.
- `containers/getaround/app/streamlit/`: production dashboard app.
- `containers/getaround/app/mlflow/`: MLflow service container files.
- `streamlit_dev/`: local standalone Streamlit app environment.
- `data/`: source datasets.
- `ml_models/`: model experimentation artifacts.
- `model_final.py`: model training/logging script.

## Run locally (production-like stack)

```bash
cd containers/getaround
cp .env.example .env
# fill all change-me values
docker compose build
docker compose up -d
```

## VPS deployment quickstart

1. Copy `containers/getaround/.env.example` to `containers/getaround/.env`.
2. Replace all `change-me` values with strong secrets.
3. Configure DNS records for the hostnames used in `.env`.
4. Run:

```bash
cd containers/getaround
docker compose build
docker compose up -d
```

Security highlights:

- Traefik insecure dashboard mode is disabled.
- MinIO bucket is initialized without anonymous download policy.
- Secrets are environment-driven and should never be committed.

## API usage example

Python:

```python
import requests

payload = {
    "model_key": "Citroen",
    "mileage": 150000,
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
    "winter_tires": True,
}

r = requests.post("https://api.pryda.dev/prediction", json=payload, timeout=30)
print(r.json())
```

curl:

```bash
curl -X POST "https://api.pryda.dev/prediction" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "model_key": "Citroen",
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
```

## Notes

- The prediction endpoint depends on the configured `MODEL_URI` artifact availability in MLflow.
- The repository is designed as a portfolio project with production-oriented engineering practices, not just model experimentation.
