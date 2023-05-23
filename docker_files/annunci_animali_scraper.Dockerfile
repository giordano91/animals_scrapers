FROM python:3.8-alpine3.18

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip --no-cache-dir -r requirements.txt

RUN mkdir -p scrapers/common
COPY scrapers/common scrapers/common

RUN mkdir -p scrapers/annunci_animali
COPY scrapers/annunci_animali scrapers/annunci_animali

ENV PYTHONPATH "${PYTHONPATH}:/scrapers"
ENV PYTHONUNBUFFERED 1