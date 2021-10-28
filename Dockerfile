FROM python:3.8-alpine

EXPOSE 5000

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app
COPY main.py /app
COPY venv/Templates /app/templates
COPY venv/static /app/static
COPY blockSchedule.txt /app

CMD [ "python", "./main.py", "production" ]