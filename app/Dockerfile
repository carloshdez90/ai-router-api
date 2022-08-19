FROM python:3.9.13-slim-bullseye

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers", "--workers", "2"]