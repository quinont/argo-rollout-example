FROM python:3.9.18-alpine3.18

WORKDIR /app

RUN apk add git && rm -rf /var/cache/apk/*

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY ./main.py /app/main.py

CMD ["python3", "main.py"]
