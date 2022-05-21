FROM python:3.7.9-stretch

ENV TZ=Asia/Bangkok
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
