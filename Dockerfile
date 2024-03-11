FROM python:3.9

RUN apt-get update && \
    apt-get install git
# RUN apk update && apk add git

WORKDIR /workspace/

COPY . /workspace/

RUN pip install -U pip && \
    pip install -r requirements.txt

EXPOSE 60133