FROM continuumio/miniconda3

# set build-time proxy settings from docker-compose.yaml#args
ARG NO_PROXY
ARG HTTP_PROXY
ARG HTTPS_PROXY

# copy build-time proxy-settings into run-time ones
ENV NO_PROXY=$NO_PROXY
ENV HTTP_PROXY=$HTTP_PROXY
ENV HTTPS_PROXY=$HTTPS_PROXY

RUN echo http proxy: ${http_proxy} ${HTTP_PROXY} \
    && echo https proxy: ${https_proxy} ${HTTPS_PROXY}

# Local-specific script to set up corporate proxy etc
ARG SSL_CERT_FILE
ENV SSL_CERT_FILE=$SSL_CERT_FILE
ENV REQUESTS_CA_BUNDLE=$SSL_CERT_FILE
COPY .setup-scripts* /.setup-scripts
RUN /.setup-scripts/debian.sh || true

# workaround for psutil installation problem: command 'gcc' failed
RUN apt-get update && apt-get install -y \
      build-essential python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN pip install --no-binary :all: --compile psutil

COPY docker/celeryworker/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ENV C_FORCE_ROOT=1

ARG env
RUN bash -c "if [ $env == 'dev' ] ; then pip install jupyterlab ; fi"
ENV env=$env

COPY docker/celeryworker/start.sh /
WORKDIR /

# install watchdog to auto-reload celery worker
RUN pip install watchdog pyyaml argh

# dir for task revoke persistency
RUN mkdir /var/run/celery/

# in docker-compose-dev we mount this as volume for live reload on changes for debugging
COPY backend/app /app

CMD ["bash", "/start.sh"]
