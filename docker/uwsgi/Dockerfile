FROM python:3

# Install deb packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
 && rm -rf /var/lib/apt/lists/*

# Install python packages
COPY svh /www/svh
WORKDIR /www/svh
RUN chown www-data:www-data -R /www/

RUN pip install -r requirements.txt --compile

ENTRYPOINT ["./run.sh"]

