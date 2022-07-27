FROM python:3.8

WORKDIR /ui

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY src .

CMD python ./src/app.py
