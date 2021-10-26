FROM python:3.8-alpine

EXPOSE 2328

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py /app
COPY Templates /app/templates
COPY blockSchedule.txt /app
COPY blockSchedule.txt /app

CMD [ "python", "./main.py", "production" ]