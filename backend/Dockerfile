FROM python:3.11.9-alpine3.20
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "main.py"]
