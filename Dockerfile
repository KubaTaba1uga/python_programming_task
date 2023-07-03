FROM python:3.11.4-slim-bullseye

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY start.py .env .
COPY src ./src

EXPOSE 8080
CMD ["./start.py"]
