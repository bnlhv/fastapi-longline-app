# Python base image
FROM python:3.9-alpine

# Define where the app would go and live
WORKDIR /app

# Install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8001