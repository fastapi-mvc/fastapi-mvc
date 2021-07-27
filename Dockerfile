FROM alpine@sha256:def822f9851ca422481ec6fee59a9966f12b351c62ccb9aca841526ffaa9f748
LABEL maintainer="Radosław Szamszur, radoslawszamszur@gmail.com"

COPY . /fastapi-mvc-template

RUN apk add gcc clang build-base python3 python3-dev py3-pip && \
    pip install /fastapi-mvc-template

EXPOSE 8000/tcp

STOPSIGNAL SIGINT

CMD ["/usr/bin/fastapi", "serve", "--host", "0.0.0.0"]
