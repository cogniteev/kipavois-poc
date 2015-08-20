FROM cogniteev/elasticdump:0.14.3

ADD kibana-data.json /data/
ADD kibana-mapping.json /data/
ADD docker-entrypoint.sh /


ENTRYPOINT ["/docker-entrypoint.sh"]
