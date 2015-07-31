FROM logstash:1.4.2

ADD employees.csv /tmp/employees.csv
ADD logstash.conf /etc/logstash/conf.d/logstash.conf

CMD logstash --debug -f /etc/logstash/conf.d
