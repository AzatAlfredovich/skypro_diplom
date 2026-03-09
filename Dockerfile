FROM python:3.12-slim

WORKDIR /library_proj

#Установка зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /library_proj/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /library_proj/

#Создаем и даем права на директорию для статических файлов
RUN mkdir -p /library_proj/staticfiles && chmod -R 755 /library_proj/staticfiles

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]