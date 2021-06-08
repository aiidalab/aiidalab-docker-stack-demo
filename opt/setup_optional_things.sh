# Setup pseudopotentials.
if [ ! -e /home/${SYSTEM_USER}/SKIP_IMPORT_PSEUDOS ]; then
   verdi data upf listfamilies | grep 'SSSP_1.1_efficiency'|| verdi import -n /opt/pseudos/SSSP_efficiency_pseudos.aiida
   verdi data upf listfamilies | grep 'SSSP_1.1_precision' || verdi import -n /opt/pseudos/SSSP_precision_pseudos.aiida
fi


# Quantum Espresso app.
if [ ! -e /home/${SYSTEM_USER}/apps/quantum-espresso ]; then
  git clone https://github.com/aiidalab/aiidalab-qe.git /home/${SYSTEM_USER}/apps/quantum-espresso
  cd /home/${SYSTEM_USER}/apps/quantum-espresso
  git checkout develop
  cd -
fi


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



