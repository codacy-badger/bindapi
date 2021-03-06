FROM python:3.7-slim

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    nginx \
    python3-dev \
    build-essential

WORKDIR /app

COPY . /app/
COPY nginx.conf /etc/nginx

RUN pip install -r requirements.txt --src /usr/local/src
RUN chmod +x ./startup.sh

EXPOSE 80

CMD [ "./startup.sh" ]
