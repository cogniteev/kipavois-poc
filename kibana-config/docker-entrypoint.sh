#!/bin/sh -e

if [ "x${ELASTICSEARCH_PORT_9200_TCP_PORT}" = x ] ; then
  echo >&2 "Error: elasticsearch container does not seem to be linked."
  exit 1
fi

ELASTICSEARCH_URL="http://elasticsearch:${ELASTICSEARCH_PORT_9200_TCP_PORT}"

# Wait for Elasticsearch
for i in `seq 60` ; do
  if curl -s "$ELASTICSEARCH_URL" | grep -q lucene_version ; then
    break
  fi
  sleep 1
done
echo >&2 'Elasticsearch node is up'

if ! curl -s "${ELASTICSEARCH_URL}"/_cat/indices | grep -q " open .kibana" ; then
  echo ".kibana index is missing. Initializing it"
  elasticdump \
    --debug \
    --input=/data/kibana-mapping.json \
    --output=http://elasticsearch:${ELASTICSEARCH_PORT_9200_TCP_PORT}/.kibana \
    --type=mapping

  elasticdump \
    --debug \
    --input=/data/kibana-data.json \
    --output=http://elasticsearch:${ELASTICSEARCH_PORT_9200_TCP_PORT}/.kibana \
    --type=data
else
  echo ".kibana index already exists. Nothing to do."
fi
