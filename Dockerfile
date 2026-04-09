# Stage 1: build dependencies
FROM python:3.12-alpine AS builder

RUN apk add --no-cache gcc musl-dev postgresql-dev

WORKDIR /app
COPY requirements.txt .
RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt


# Stage 2: final image
FROM python:3.12-alpine

RUN apk add --no-cache libpq

ENV PATH="/venv/bin:$PATH"

WORKDIR /app
COPY --from=builder /venv /venv
COPY . .

EXPOSE 8080
CMD ["python", "main.py"]
