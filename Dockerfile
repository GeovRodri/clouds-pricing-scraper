FROM ubuntu:latest

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN apt-get install -y libffi-dev \
            libxml2 \
            gcc \
            libpng-dev \
            libxml2-dev \
            libxslt-dev

WORKDIR /app
COPY . /app
RUN pip3 install --upgrade pip setuptools
RUN pip3 install uwsgi
RUN pip3 install -r /app/requirements.txt
EXPOSE 80
CMD ["uwsgi", "--plugin", "python3", "--ini", "/app/wsgi.ini"]