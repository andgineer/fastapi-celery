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

RUN apt-get update

#RUN conda install -c conda-forge rdkit

RUN conda install pip

COPY docker/tests/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ARG env
RUN bash -c "if [ $env == 'dev' ] ; then pip install jupyterlab ; fi"
ENV env=$env

# we mount this as volume for live reload on changes for debugging
COPY backend /backend

ENV PYTHONPATH=/
WORKDIR /backend

COPY docker/tests/start.sh /
RUN chmod +x /*.sh
CMD /start.sh
