FROM mher/flower

# set build-time proxy settings from docker-compose.yaml#args
ARG NO_PROXY
ARG HTTP_PROXY
ARG HTTPS_PROXY

# copy build-time proxy-settings into run-time ones
ENV NO_PROXY=$NO_PROXY
ENV HTTP_PROXY=$HTTP_PROXY
ENV HTTPS_PROXY=$HTTPS_PROXY


CMD ["flower", "--broker=amqp://guest:guest@rabbitmq:5672/"]
