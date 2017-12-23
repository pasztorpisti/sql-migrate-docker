FROM alpine:3.6

ENV SQL_MIGRATE_VERSION=v1.0.0

RUN apk add --no-cache --update openssl \
    && wget -qO /tmp/sql-migrate.zip https://github.com/pasztorpisti/sql-migrate/releases/download/${SQL_MIGRATE_VERSION}/sql-migrate-linux-amd64.zip \
	&& cd /usr/local/bin \
    && unzip -qo /tmp/sql-migrate.zip \
    && rm /tmp/sql-migrate.zip \
    && chmod +x sql-migrate

ENTRYPOINT ["sql-migrate"]
