FROM python:3.12-slim

LABEL authors="mikeonuf"

WORKDIR /project_root

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY .env .

CMD ["python", "app/main.py"]