FROM python:3-alpine
LABEL authors="mikeonuf"
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY /.venv /app
CMD ["python", "app/main.py"]