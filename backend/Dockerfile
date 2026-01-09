# syntax=docker/dockerfile:1

FROM public.ecr.aws/docker/library/python:3.13-slim-bullseye
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Run migrations and collect static files
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate && gunicorn app.wsgi:application --bind 0.0.0.0:8000 --workers 4"]