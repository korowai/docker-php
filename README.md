# korowai/docker-php

Docker container with PHP for korowai project.

### Build arguments & environment variables

The container defines several build arguments which are copied to corresponding
environment variables within the running container. All the arguments/variables
have names starting with `PHP_` prefix. All the scripts respect these
variables, so the easiest way to adjust the container to your needs is to set
environment variables (`-e` flag to [docker](https://docker.com/)). There are
some exceptions currently -- `SPHINX_UID`, `SPHINX_GID`,
`SPHINX_AUTOBUILD_PORT`, `SPHINX_VERSION`, `SPHINX_AUTOBUILD_VERSION`, and
`SPHINX_RTD_THEME_VERSION` must be defined at build time, so they
may only be changed via docker's build arguments.

| Argument                    | Default Value        | Description                                                  |
| --------------------------- | -------------------- | ------------------------------------------------------------ |
| PHP\_UID                    | 1000                 | UID of the user running commands within the container (cli). |
| PHP\_GID                    | 1000                 | GID of the user running commands within the container (cli). |

### Software included

  - [PHP](https://php.net/)
  - [php-ldap](https://www.php.net/manual/en/book.ldap.php)
  - [composer](https://getcomposer.org/)
