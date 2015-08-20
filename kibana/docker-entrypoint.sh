#!/bin/bash

set -e

# Add kibana as command if needed
if [[ "$1" == -* ]]; then
	set -- kibana "$@"
fi

# Run as user "kibana" if the command is "kibana"
if [ "$1" = 'kibana' ]; then
	if [ "$ELASTICSEARCH_URL" -o "$ELASTICSEARCH_PORT_9200_TCP" ]; then
		: ${ELASTICSEARCH_URL:='http://elasticsearch:9200'}
		sed -ri "s!^(elasticsearch_url:).*!\1 '$ELASTICSEARCH_URL'!" /opt/kibana/config/kibana.yml
	else
		echo >&2 'warning: missing ELASTICSEARCH_PORT_9200_TCP or ELASTICSEARCH_URL'
		echo >&2 '  Did you forget to --link some-elasticsearch:elasticsearch'
		echo >&2 '  or -e ELASTICSEARCH_URL=http://some-elasticsearch:9200 ?'
		echo >&2
	fi

  # Wait for Elasticsearch
  for i in `seq 60` ; do
    if curl -s "$ELASTICSEARCH_URL" | grep -q lucene_version ; then
      break
    fi
    sleep 1
  done
  echo >&2 'Elasticsearch node is up'
  # Wait for .kibana index to be created if necessary
  for i in `seq 60` ; do
    if curl -s "${ELASTICSEARCH_URL}"/_cat/indices | grep -q " open .kibana" ; then
      break
    fi
    sleep 1
  done
  echo >&2 '.kibana index is opened'

	set -- gosu kibana "$@"
fi

exec "$@"
