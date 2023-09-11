FROM python:3.8-alpine as python
RUN apk update
RUN apk add --no-cache make automake gcc g++ subversion python3-dev python3

RUN apk --update add build-base libxslt-dev

RUN apk add --virtual .build-deps \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        gcc libc-dev geos-dev geos && \
    runDeps="$(scanelf --needed --nobanner --recursive /usr/local \
    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
    | xargs -r apk info --installed \
    | sort -u)" && \
    apk add --virtual .rundeps $runDeps

RUN geos-config --cflags

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "./sentiment_analyzer.py"]
