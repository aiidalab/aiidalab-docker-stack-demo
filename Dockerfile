FROM aiidalab/aiidalab-docker-stack:22.8.0

WORKDIR /opt/

RUN chmod 755 /etc/container_environment
RUN chmod 644 /etc/container_environment.sh /etc/container_environment.json

RUN cd aiidalab-home && \
  git fetch && \
  git checkout materials-marketplace && \
  cd .. && chmod 774 aiidalab-home
