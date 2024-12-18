FROM python:3.10-slim

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy your code and workspace to /opt/dagster/app
COPY pyproject.toml workspace.yaml /opt/dagster/app/
COPY energy_mix /opt/dagster/app/energy_mix

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

# Copy dagster instance YAML to $DAGSTER_HOME
COPY .dagster/dagster.yaml /opt/dagster/dagster_home/

WORKDIR /opt/dagster/app

EXPOSE 3000

ENTRYPOINT ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000"]
