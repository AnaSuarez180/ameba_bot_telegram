FROM python:3.10.8 AS bot

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100


RUN apt-get update
RUN apt-get install -y python3 python3-pip python-dev build-essential python3-venv && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app/

RUN pip3 install -r requirements.txt

CMD python3 bot.py