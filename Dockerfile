# hadolint global ignore=DL3008,DL3013,DL4006
FROM docker.io/python:3.12-slim-bookworm

RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y libpq-dev \
  && apt-get install -y gettext \
  && apt-get -y install cron \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY hello-cron.sh /etc/cron.d/hello-cron
RUN chmod 0644 /etc/cron.d/hello-cron
RUN crontab /etc/cron.d/hello-cron
RUN touch /var/log/cron.log

WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 -m pip install -U --disable-pip-version-check .[non-termux]w

COPY . .
RUN chmod +x /usr/src/app/entrypoint.sh
CMD ["/usr/src/app/entrypoint.sh"]