FROM python:3.11.4-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY start.py .
COPY src ./src

EXPOSE 8080

CMD ["./start.py"]
