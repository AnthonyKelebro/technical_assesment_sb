#!/bin/bash

set -e

# # Add test data to access log for avoiding zero log error
echo '172.17.0.1 - - [07/Jun/2022:20:32:05 +0000] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36" "-"' > /var/log/nginx/access.log

# Change permission for firebeat yml files
chmod go-w /etc/filebeat/filebeat.yml
chmod go-w /etc/filebeat/modules.d/nginx.yml

# Sleep 2 min for avoiding init ELK stack process
sleep 120

# Initialize filebeat
filebeat modules enable nginx
filebeat setup
filebeat -e
