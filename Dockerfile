FROM python:3.11-slim

WORKDIR /app 

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app

# CMD ["gunicorn", "-w", "4", "-b","0.0.0.0:8000", "app:app"]

CMD ["python", "app.py"]
