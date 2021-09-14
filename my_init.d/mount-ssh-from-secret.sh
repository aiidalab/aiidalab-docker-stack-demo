#!/bin/bash -eux

if [ ! -d /home/${SYSTEM_USER}/.ssh/ ] && [ -f /run/secrets/ssh_key ]; then
  mkdir --mode=0700 /home/${SYSTEM_USER}/.ssh/
  touch /home/${SYSTEM_USER}/.ssh/known_hosts
  # Linking ssh key from secret.
  cp /run/secrets/ssh_key /home/${SYSTEM_USER}/.ssh/id_rsa

  # Try to fix permissions (should fail when user was not yet created).
  chown -R ${SYSTEM_USER}:${SYSTEM_USER} /home/${SYSTEM_USER}/.ssh || echo "initial startup"
fi
