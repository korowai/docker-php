#############################################################################
# NOTE: FILE GENERATED AUTOMATICALLY, DO NOT EDIT!!!
#############################################################################


FROM php:7.3-cli-stretch
MAINTAINER Paweł Tomulik <ptomulik@meil.pw.edu.pl>

ARG PHP_UID=1000
ARG PHP_GID=1000

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

LABEL org.label-schema.build-date="${BUILD_DATE}" \
      org.label-schema.name="Docker PHP Image" \
      org.label-schema.description="Docker image with PHP CLI for Korowai project." \
      org.label-schema.vcs-ref="${VCS_REF}" \
      org.label-schema.vcs-url="https://github.com/korowai/docker-php" \
      org.label-schema.vendor="Paweł Tomulik" \
      org.label-schema.version="${VERSION}" \
      org.label-schema.schema-version="1.0"


ENV PHP_UID=$PHP_UID \
    PHP_GID=$PHP_GID

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      unzip \
      libldap2-dev \
      libsasl2-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    curl -L https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer && \
    curl -L https://github.com/jwilder/dockerize/releases/download/v0.6.0/dockerize-linux-amd64-v0.6.0.tar.gz \
         --output /tmp/dockerize-linux-amd64-v0.6.0.tar.gz && \
    tar -C /usr/local/bin -zxvf /tmp/dockerize-linux-amd64-v0.6.0.tar.gz && \
    rm -f /tmp/dockerize-linux-amd64-v0.6.0.tar.gz && \
    docker-php-ext-configure ldap --with-libdir=lib/x86_64-linux-gnu --with-ldap-sasl && \
    docker-php-ext-install ldap && \
    groupadd -g $PHP_GID php && \
    useradd -m -g php --uid $PHP_UID php

VOLUME /home/php/project

USER php

WORKDIR /home/php/project

# vim: set ft=dockerfile:
