FROM python:3.8-alpine3.18

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip --no-cache-dir -r requirements.txt

RUN mkdir -p scrapers/common
COPY scrapers/common scrapers/common

RUN mkdir -p scrapers/my_pet_24
COPY scrapers/my_pet_24 scrapers/my_pet_24

ENV PYTHONPATH "${PYTHONPATH}:/scrapers"
ENV PYTHONUNBUFFERED 1