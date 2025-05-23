FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv/celery

COPY ./app app
COPY ./requirements.txt /tmp/requirements.txt
COPY ./celery.sh celery.sh

RUN pip install --no-cache-dir \
    -r /tmp/requirements.txt

VOLUME ["/var/log/celery", "/var/run/celery"]

CMD ["./celery.sh"]