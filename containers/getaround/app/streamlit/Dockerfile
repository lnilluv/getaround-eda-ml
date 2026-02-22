FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

CMD ["streamlit", "run", "--server.port", "8501", "--server.address", "0.0.0.0", "app.py"]
