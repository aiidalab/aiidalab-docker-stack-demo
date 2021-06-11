# Setup pseudopotentials.
if [ ! -e /home/${SYSTEM_USER}/SKIP_IMPORT_PSEUDOS ]; then
  aiida-pseudo install sssp -x PBE -p efficiency
  aiida-pseudo install sssp -x PBE -p precision
  aiida-pseudo install sssp -x PBEsol -p efficiency
  aiida-pseudo install sssp -x PBEsol -p precision
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

# Manually install and enable widget_bandsplot (not clear why this is necessary)
/opt/conda/bin/python -m pip install widget_bandsplot
jupyter nbextension enable --py widget_bandsplot

