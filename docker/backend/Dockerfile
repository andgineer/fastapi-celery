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

# Conditional certificate setup
RUN if [ -n "$SSL_CERT_FILE" ] && [ -f "$SSL_CERT_FILE" ]; then \
    echo "Using custom certificate: $SSL_CERT_FILE" && \
    export SSL_CERT_FILE=$SSL_CERT_FILE && \
    export REQUESTS_CA_BUNDLE=$SSL_CERT_FILE; \
    else \
    echo "Using system certificates" && \
    export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt && \
    export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt; \
    fi

COPY .setup-scripts* /.setup-scripts
RUN /.setup-scripts/debian.sh || true

# workaround for psutil installation problem: command 'gcc' failed
RUN apt-get update && apt-get install -y \
      build-essential python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN pip install --no-binary :all: --compile psutil

#RUN conda install -c conda-forge rdkit

RUN conda install pip \
    && pip install uvicorn gunicorn

COPY docker/backend/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ARG env
RUN bash -c "if [ $env == 'dev' ] ; then pip install jupyterlab ; fi"
ENV env=$env

# in docker-compose-dev we mount this as volume for live reload on changes for debugging
COPY backend /backend
VOLUME /backend

WORKDIR /backend
EXPOSE 80

COPY docker/backend/start.sh /
RUN chmod +x /*.sh
CMD /start.sh
