FROM python:2.7.10
RUN apt-get update && apt-get install -y \
  build-essential \
  python-dev \
  uwsgi \
  uwsgi-plugin-python \
  virtualenv
# workaround https://bugs.launchpad.net/ubuntu/+source/python2.7/+bug/1115466
RUN ln -s /usr/lib/python2.7/plat-*/_sysconfigdata_nd.py /usr/lib/python2.7/

# Prepare virtualenv
RUN virtualenv /code/.env
WORKDIR /code
ADD requirements.txt /code/
RUN .env/bin/pip install -r requirements.txt

# Add application code
ADD . /code

EXPOSE 5000
CMD uwsgi \
  --plugin python \
  --socket 0.0.0.0:5000 \
  --wsgi-file app.py --callable app \
  --virtualenv /code/.env \
  --processes 4 --threads 2
