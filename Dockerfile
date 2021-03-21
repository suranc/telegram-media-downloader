FROM python:3

ADD requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app
ADD tmd.py /app

ENTRYPOINT /app/tmd.py