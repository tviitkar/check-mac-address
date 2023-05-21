#!/bin/bash
python3 mac_verifier.py &
prometheus --config.file=/etc/prometheus/prometheus.yml &
node_exporter