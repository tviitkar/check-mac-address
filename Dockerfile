FROM python:3.11-alpine3.18

# Just for fun
LABEL MAINTAINER="Tambet Viitkar"
LABEL description="Für Elisa - Mac Address Verifier"

# Working directory
WORKDIR /python_mac

# Copy dependencies to the image
COPY ./requirements.txt /python_mac/requirements.txt

# Install (solve) Python dependencies
RUN pip install -r requirements.txt

# Copy all files from local working folder to the image
COPY . /python_mac

# Flask is set to run on port 5000 in the script
# Therefor I probably don't need this
# Keeping it here for reference (for now)
# EXPOSE 5000

# Executable that will run after the container is initiated
ENTRYPOINT ["python3"]

# Run Python script
CMD ["mac_address.py"]