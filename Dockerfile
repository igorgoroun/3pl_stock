FROM odoo:17
USER root

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential

RUN pip3 install --upgrade pip
RUN pip3 install requests paramiko

