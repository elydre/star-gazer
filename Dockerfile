FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget

RUN pip install cryptography

RUN mkdir /app

WORKDIR /app

RUN mkdir /app/fworker
RUN mkdir /app/mod


RUN wget "https://raw.githubusercontent.com/pf4-DEV/star-gazer/main/files/worker.py" -O /app/worker.py
RUN wget "https://raw.githubusercontent.com/pf4-DEV/POOcom/main/POOcom.py" -O /app/mod/POOcom.py
RUN wget "https://raw.githubusercontent.com/pf4-DEV/star-gazer/main/files/mod/util.py" -O /app/mod/util.py
RUN wget "https://raw.githubusercontent.com/pf4-DEV/star-gazer/main/files/fworker/code.py" -O /app/fworker/code.py
RUN echo "6rNQ4x9kMtzRd6drBhZOMOj0eyoiqL1-rCC0JvKgJhY=" > /app/mod/key.txt

# lancer le worker au démarrage du container
CMD ["python3", "/app/worker.py"]
