FROM python:3.9.16-alpine

WORKDIR /app

COPY *.py .
COPY requirements.txt .

ENV TERM xterm
ENV PYTHONUNBUFFERED 1

ARG TARGETPLATFORM
ARG BUILD_DATE
ARG COMMIT

RUN python -m pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    apk add --no-cache build-base && \
    apk add --no-cache linux-headers && \
    if [ "$TARGETPLATFORM" = "linux/arm/v6" ] || [ "$TARGETPLATFORM" = "linux/arm/v7" ]; then \
        apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev; \
    fi && \
    pip install gunicorn && \
    pip install -r requirements.txt && \
    apk del build-base && \
    if [ "$TARGETPLATFORM" = "linux/arm/v6" ] || [ "$TARGETPLATFORM" = "linux/arm/v7" ]; then \
        apk del .build-deps; \
    fi

EXPOSE 5000

LABEL maintainer="Discord: the_devil_of_the_rhine (863687441809801246)"
LABEL commit=$COMMIT
LABEL description="Simple Chatserver with file upload."
LABEL release=$BUILD_DATE
LABEL VERSION="0.1.0"
LABEL url="https://gitlab.bloodygang.com/Serpensin"

CMD ["gunicorn", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "4", "Server:app", "-b", ":5000"]
