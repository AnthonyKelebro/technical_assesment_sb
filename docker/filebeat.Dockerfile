FROM debian:bullseye-slim

ARG FILEBEAT_VERSION
ARG ELASTIC_USERNAME
ARG ELASTIC_PASSWORD

ENV EL_USER=$ELASTIC_USERNAME
ENV EL_PASS=$ELASTIC_PASSWORD

COPY files/filebeat/filebeat_init.sh /usr/bin/filebeat_init.sh

RUN apt-get update && \
    apt-get install -y wget && \
    wget https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-$FILEBEAT_VERSION-amd64.deb -o /tmp/filebeat-$FILEBEAT_VERSION-amd64.deb && \
    dpkg -i /tmp/filebeat-$FILEBEAT_VERSION-amd64.deb && \
    chmod +x /usr/bin/filebeat_init.sh && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/* && \
    rm -rf /tmp/*    

COPY files/filebeat/filebeat.yml /etc/filebeat/filebeat.yml
COPY files/filebeat/nginx.yml /etc/filebeat/modules.d/nginx.yml

ENTRYPOINT [ "/bin/bash", "-c", "/usr/bin/filebeat_init.sh;" ]
