FROM aiidalab/aiidalab-docker-stack:22.8.0

WORKDIR /opt/

RUN cd aiidalab-home && \
  git fetch && \
  git checkout materials-marketplace && \
  cd .. && chmod 774 aiidalab-home
