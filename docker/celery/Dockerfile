FROM python:3

# Install deb packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gettext \
    graphviz \
    postgresql-client \
    ffmpeg \
    dos2unix \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /www/svh


# Install python packages
COPY svh/requirements.txt ./
RUN pip3 install -r requirements.txt --compile

# Copy project files
COPY svh .

# Create local settings
RUN mkdir /www/svh/svh/settings_local/ && \
    touch /www/svh/svh/settings_local/__init__.py && \
    chown www-data:www-data -R /www/ && \
    dos2unix ./run_celery.sh

USER www-data
ENTRYPOINT ["./run_celery.sh"]
