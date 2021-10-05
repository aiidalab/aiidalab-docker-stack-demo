#!/bin/bash
set -e
set -u

# Manually install and enable widget_bandsplot (not clear why this is necessary)
/opt/conda/bin/python -m pip install widget_bandsplot
jupyter nbextension enable --py widget_bandsplot

