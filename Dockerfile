FROM node:18.12.1 as builder-client

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
ADD ./client/package.json /app/package.json
ADD ./client/package-lock.json /app/package-lock.json
RUN npm install -g npm@9.8.1 && npm install --save

# copy all
COPY ./client /app/

# build
RUN npm run build-only

FROM python:3.11-buster as builder-server

ENV POETRY_VERSION=1.6.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY ./server/pyproject.toml ./server/poetry.lock ./
RUN touch README.md

RUN poetry install --no-root

FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update &&  \
    apt-get install -y nginx supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN rm -rf /usr/share/nginx/html/*
COPY nginx.conf /etc/nginx/nginx.conf

COPY --from=builder-server ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY ./server ./app

COPY --from=builder-client /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["/usr/bin/supervisord"]
