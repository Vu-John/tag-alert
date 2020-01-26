FROM python:3.6-alpine

RUN adduser -D tag-alert

WORKDIR /home/tag-alert

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN venv/bin/pip install gunicorn psycopg2-binary psycopg2

COPY app app
COPY migrations migrations
COPY tag_alert.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP tag_alert.py

RUN chown -R tag-alert:tag-alert ./
USER tag-alert

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
