FROM python:3.11-alpine3.18

# Just for fun
LABEL MAINTAINER="Tambet Viitkar"
LABEL description="Für Elisa - Mac Address Verifier"

# Set working directory
WORKDIR /app

# Copy Python requirements to image and solve dependencies
COPY ./python/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy all files from local working folder to the image
COPY ./python /app

# Update packages, install Prometheus and create configuration file
RUN apk update && apk upgrade --no-cache
RUN apk add prometheus prometheus-node-exporter
COPY /misc/prometheus.yml /etc/prometheus/

# Copy services script to image and make it executable
COPY ./misc/run_services.sh /app/run_services.sh
RUN chmod +x /app/run_services.sh

# Run the services script that start Flask and Prometheus
ENTRYPOINT ["/bin/sh"]
CMD ["/app/run_services.sh"]