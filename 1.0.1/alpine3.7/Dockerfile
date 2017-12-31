FROM alpine:3.7

ENV SQL_MIGRATE_VERSION=v1.0.1

RUN cd /usr/local/bin \
    && wget -qO- https://github.com/pasztorpisti/sql-migrate/releases/download/${SQL_MIGRATE_VERSION}/sql-migrate-linux-amd64.zip | unzip -q - \
    && chmod +x sql-migrate

ENTRYPOINT ["sql-migrate"]
