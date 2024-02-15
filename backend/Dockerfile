# Image pour adapter les dépendances
FROM weastur/poetry:latest-python-3.11-alpine as requirements

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without test

# Image finale
FROM python:3.11-alpine

WORKDIR /app

COPY --from=requirements /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

EXPOSE 8080

CMD ["uvicorn", "sae_backend:app", "--workers", "4", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers", "--forwarded-allow-ips='*'"]
