ARG PYTHON_VERSION=3.12

FROM python:$PYTHON_VERSION-alpine AS build

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apk add --update --no-cache curl unzip py3-pip build-base python3-dev libpq-dev linux-headers
RUN pip install --no-cache-dir --upgrade pip
RUN \
    apk add --no-cache curl unzip ca-certificates && \
    VERSION="$(curl -fsSL https://api.github.com/repos/XTLS/Xray-core/releases/latest | \
        grep '"tag_name":' | \
        sed -E 's/.*"([^"]+)".*/\1/')" && \
    curl -fL \
        "https://github.com/XTLS/Xray-core/releases/download/${VERSION}/Xray-linux-64.zip" \
        -o /tmp/xray.zip && \
    mkdir -p /tmp/xray /usr/local/share/xray && \
    unzip -q /tmp/xray.zip -d /tmp/xray && \
    install -m 0755 /tmp/xray/xray /usr/local/bin/xray && \
    if [ -f /tmp/xray/geoip.dat ]; then \
        install -m 0644 /tmp/xray/geoip.dat /usr/local/share/xray/geoip.dat; \
    fi && \
    if [ -f /tmp/xray/geosite.dat ]; then \
        install -m 0644 /tmp/xray/geosite.dat /usr/local/share/xray/geosite.dat; \
    fi && \
    rm -rf /tmp/xray /tmp/xray.zip

COPY ./requirements.txt /code/
RUN pip install --upgrade pip setuptools \
    && pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN rm -rf /var/cache/apk/*

FROM python:$PYTHON_VERSION-alpine

ENV PYTHON_LIB_PATH=/usr/local/lib/python${PYTHON_VERSION%.*}/site-packages
WORKDIR /code

RUN rm -rf $PYTHON_LIB_PATH/*
RUN apk add --no-cache bash curl
RUN apk add --no-cache --upgrade

COPY --from=build $PYTHON_LIB_PATH $PYTHON_LIB_PATH
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /usr/local/share/xray /usr/local/share/xray

COPY . /code

RUN ln -s /code/marzban-cli.py /usr/bin/marzban-cli
RUN chmod +x /usr/bin/marzban-cli
RUN marzban-cli completion install --shell bash

CMD ["bash", "-c", "alembic upgrade head; python main.py"]
