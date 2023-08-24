FROM python:3.11-slim

ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

# CMD ["gunicorn", "-w", "4", "-b","0.0.0.0:8000", "app:app"]

# CMD ["python", "app.py"]

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app

