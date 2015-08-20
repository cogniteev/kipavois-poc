FROM nginx:1.9.4

RUN apt-get update && apt-get install -y apache2-utils

RUN htpasswd -b -c /etc/nginx/.htpasswd admin admin && \
    htpasswd -b /etc/nginx/.htpasswd google google && \
    htpasswd -b /etc/nginx/.htpasswd facebook facebook && \
    htpasswd -b /etc/nginx/.htpasswd linkedin linkedin && \
    htpasswd -b /etc/nginx/.htpasswd apple apple

COPY nginx.conf /etc/nginx/nginx.conf
