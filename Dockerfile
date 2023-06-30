FROM python:3.11.4-slim-bullseye

COPY pyproject.toml setup.py start.py /app/
COPY src /app/src
RUN pip install -e /app/

EXPOSE 8080

CMD ["/app/start.py"]
