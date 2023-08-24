FROM python:3.11-slim

ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

ADD https://github.com/pgzm29/m7api/raw/ba52b73aedd7e284a129472cc74da59f77c22432/pneumonia_model.keras ./

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app

