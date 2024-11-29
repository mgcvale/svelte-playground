FROM python:3.10-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpcre3-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./app.py ./requirements.txt ./uwsgi.ini ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uwsgi", "--ini", "uwsgi.ini"]

