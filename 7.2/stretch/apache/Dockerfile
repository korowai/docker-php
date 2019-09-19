#############################################################################
# NOTE: FILE GENERATED AUTOMATICALLY, DO NOT EDIT!!!
#############################################################################


FROM php:7.2-apache-stretch
MAINTAINER Paweł Tomulik <ptomulik@meil.pw.edu.pl>



ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

LABEL org.label-schema.build-date="${BUILD_DATE}" \
      org.label-schema.name="Docker PHP+Apache Image" \
      org.label-schema.description="Docker image with PHP and Apache for Korowai project." \
      org.label-schema.vcs-ref="${VCS_REF}" \
      org.label-schema.vcs-url="https://github.com/korowai/docker-php" \
      org.label-schema.vendor="Paweł Tomulik" \
      org.label-schema.version="${VERSION}" \
      org.label-schema.schema-version="1.0"




RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      unzip \
      openssh-client \
      libldap2-dev \
      libsasl2-dev \
      ssl-cert && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    curl -L https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer && \
    curl -L https://github.com/jwilder/dockerize/releases/download/v0.6.0/dockerize-linux-amd64-v0.6.0.tar.gz \
         --output /tmp/dockerize-linux-amd64-v0.6.0.tar.gz && \
    tar -C /usr/local/bin -zxvf /tmp/dockerize-linux-amd64-v0.6.0.tar.gz && \
    rm -f /tmp/dockerize-linux-amd64-v0.6.0.tar.gz && \
    docker-php-ext-configure ldap --with-libdir=lib/x86_64-linux-gnu --with-ldap-sasl && \
    docker-php-ext-install ldap

ENV APACHE_DOCUMENT_ROOT /var/www/html
RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf && \
    sed -ri -e 's!/var/www/!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf && \
    sed -ri -e 's!^\s*(</VirtualHost>)\s*$!\tAllowEncodedSlashes NoDecode\n\1!' /etc/apache2/sites-available/*.conf && \
    a2enmod rewrite && \
    a2enmod ssl && \
    a2ensite default-ssl

# vim: set ft=dockerfile:
