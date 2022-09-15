FROM python:3.8-alpine

EXPOSE 2328

WORKDIR /app


COPY requirements.txt .


RUN apk update && apk add python3-dev \
                          gcc \
                          libc-dev \
                          libffi-dev


RUN pip install -r requirements.txt



COPY . /app
COPY main.py /app
COPY Templates /app/templates
COPY static /app/static
COPY blockSchedule.txt /app

CMD [ "python", "./main.py", "production" ]