FROM aiidalab/aiidalab-docker-stack:develop

USER root


# Install simulation engines.
RUN conda install --yes -c conda-forge \
  qe==6.7.0 \
  cp2k=8.2.0 \
  && conda clean --all

# Install Python packages needed for AiiDAlab and populate reentry cache for root (https://pypi.python.org/pypi/reentry/).
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN reentry scan

# Prepare user's folders for AiiDAlab launch.
COPY opt/setup_optional_things.sh /opt/
COPY my_init.d/setup_optional_things.sh /etc/my_init.d/90_setup_optional_things.sh

CMD ["/sbin/my_my_init"]
