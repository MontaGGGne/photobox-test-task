FROM python:3.10

WORKDIR /app

COPY requirements.in .
RUN python -m pip install pip-tools
RUN pip-compile
RUN pip-sync

COPY . .