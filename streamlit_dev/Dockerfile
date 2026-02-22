FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /home/app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

COPY . /home/app

RUN useradd --create-home appuser && chown -R appuser:appuser /home/app
USER appuser

CMD ["sh", "-c", "streamlit run --server.port ${PORT:-8501} --server.address 0.0.0.0 app.py"]
