FROM postgres:15

EXPOSE 5432

ENV max_connections=2

COPY ./init.sql /docker-entrypoint-initdb.d/