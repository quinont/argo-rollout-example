FROM python:3.9.18-alpine3.18

WORKDIR /app

COPY ./frontend/ /app/frontend/

COPY requirements.txt /app

RUN pip install -r requirements.txt

ENV FLASK_RUN_PORT=8080
ENV FLASK_RUN_HOST="0.0.0.0"

EXPOSE 8080

CMD ["flask", "--app", "frontend", "run"]
