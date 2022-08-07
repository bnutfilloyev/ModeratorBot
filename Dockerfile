#FROM python
#ENV BOT_NAME=$BOT_NAME
#
#WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"
#COPY requirements.txt /usr/src/app/"${BOT_NAME:-tg_bot}"
#RUN pip install -r /usr/src/app/"${BOT_NAME:-tg_bot}"/requirements.txt
#COPY . /usr/src/app/"${BOT_NAME:-tg_bot}"


FROM python:3.8.6

LABEL MAINTAINER="Bekhruz yoshlikmedia@gmail.com"

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

CMD python -u app.py
