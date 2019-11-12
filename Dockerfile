FROM python:3.7.4

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY wait-for-it.sh .
COPY ./static/ ./static/
RUN ls

CMD [ "python", "./app.py" ]
