FROM python:3.12-slim

# Dagster plus the libraries candidates need for Task 2.
RUN pip install --no-cache-dir \
    dagster==1.13.8 \
    dagster-webserver==1.13.8 \
    boto3==1.38.23 \
    psycopg2-binary==2.9.10 \
    pandas==2.2.3

ENV DAGSTER_HOME=/opt/dagster/dagster_home
RUN mkdir -p $DAGSTER_HOME && touch $DAGSTER_HOME/dagster.yaml

WORKDIR /opt/dagster/app
ENV PYTHONPATH=/opt/dagster/app

EXPOSE 3000

# `dagster dev` runs the webserver and the daemon (required for schedules).
CMD ["dagster", "dev", "-m", "dagster_project.definitions", "-h", "0.0.0.0", "-p", "3000"]
