#!/bin/bash
set -em

su "${SYSTEM_USER}" -c /opt/install-widget_bandsplot.sh
su "${SYSTEM_USER}" -c /opt/setup-quantum-espresso-code.sh

# Start background process to install the SSSP pseudo potentials:
su "${SYSTEM_USER}" -c /opt/install-sssp &
