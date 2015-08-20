This repository demonstrates usage of [cogniteev/kipavois](https://github.com/cogniteev/kipavois)
NodeJS proxy thru a Docker Compose application.

This application provides a Kibana instance, where users are only allowed to
see data they own. To achieve that, we use KiPavois NodeJS proxy to rewrite
queries sent by Kibana to Elasticsearch in order to filter-out data
the authenticated user is not allowed to read.

## Requirements

You may have installed:

* docker-compose 1.4.0 or higher
* docker registry (either on your workstation or thru docker-machine)
up and running

## Usage

To start the application:

```shell
docker-compose up
```

Then browse the following url: http://docker_registry
where *docker_registry* is:

* `localhost` if docker is installed on your workstation
* IP of your docker-machine machine. You can get it by running
`docker-machine ip <NAME>`. To get list of available machine,
use the `docker-machine ls` command.

You will be then asked to provide a login/password. See [nginx Dockerfile](nginx/Dockerfile) to get the list of valid users.

## Containers Linkage

![container dependencies](doc/containers.png)

* Logstash container pushes CSV data into Elastisearch, and then stop.
* Nginx performs basic authentication and acts as proxy for an uwsgi flask application
* Flask application processes requests as follow:
  1. adds an `x-kibana-user` HTTP header, value if the username
  authenticated in nginx. If the username is `admin`, then the HTTP header is
  not added.
  1. forward requests to KiPavois, and stream the result back to nginx
* Kibana leverage Elasticsearch to build dashboards
* KiPavois receives Elasticsearch requests made by Kibana and process
the queries as follow:
  * If the `x-kibana-user` is set:
    * requests that try to modify Kibana configuration are rejected.
    * Another filter is added to search queries so that only data that
    belongs to the authenticated user are fetched.
  * Otherwise, the request is not altered, passed to Elasticsearch and
  streamed by to Kibana.

## Rationale

Authentication is made by Nginx, and the Flask application is almost
stateless. It would be possible to specify the `x-kibana-user` directly
in nginx configuration and get rid of the Flask application.

#### So that why using Flask?

In the real use-case where KiPavois is used, Flask application is taking
care of authentication, not nginx. So the Flask container here is used to
demonstrate the [kipavois](https://pypi.python.org/pypi/kipavois/)
Python module.

## License

`KiPavois-POC` is licensed under the Apache License, Version 2.0.
See [LICENSE](LICENSE) file for full license text.
