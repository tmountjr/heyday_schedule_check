FROM python:3.9-alpine

RUN mkdir /app

WORKDIR /app

ADD main.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]