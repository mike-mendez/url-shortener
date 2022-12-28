FROM python:3.11.1-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt