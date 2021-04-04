# FROM tiangolo/uwsgi-nginx-flask:python3.6
FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8

# copy over our requirements.txt file
COPY requirements.txt /tmp/

# upgrade pip and install required python packages
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

# copy over our app code
COPY ./sfshare.wsgi /app/main.py
COPY ./application /app/application

ARG GIT_SHA_ARG
ENV GIT_SHA $GIT_SHA_ARG
