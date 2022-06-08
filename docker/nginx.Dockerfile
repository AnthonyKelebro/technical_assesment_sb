ARG NGINX_VERSION
FROM nginx:$NGINX_VERSION-alpine

RUN unlink /var/log/nginx/access.log && \
    unlink /var/log/nginx/error.log
