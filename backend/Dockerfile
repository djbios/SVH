FROM python:3

# Install deb packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client dos2unix \
 && rm -rf /var/lib/apt/lists/*

# Install python packages
COPY requirements.txt ./
RUN pip3 install -r requirements.txt --compile

COPY . /www/svh
WORKDIR /www/svh

RUN mkdir /www/svh/svh/settings_local/ && \
    touch /www/svh/svh/settings_local/__init__.py && \
    chown www-data:www-data -R /www && \
    mkdir -p /www/svh/static/ && \
    chown www-data:www-data -R /www/svh/static/ && \
    dos2unix ./run.sh

USER www-data

ENTRYPOINT ["./run.sh"]
