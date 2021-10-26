#!/bin/bash
set -e
set -u

computer_name=localhost

# Setup Quantum ESPRESSO pw.x code.
for code_name in pw projwfc dos ;
do
  verdi code show ${code_name}@${computer_name} || verdi code setup \
      --non-interactive                                             \
      --label ${code_name}                                          \
      --description "${code_name}.x AiiDAlab container."            \
      --input-plugin quantumespresso.${code_name}                   \
      --computer ${computer_name}                                   \
      --remote-abs-path `which ${code_name}.x`
done
