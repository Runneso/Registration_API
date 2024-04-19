FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY . .

# update pip python
RUN pip3 install -U pip

# install packages for the project
RUN pip3 install -r requirements.txt