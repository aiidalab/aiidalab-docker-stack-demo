import os

import aiida
from aiida.orm import load_computer


aiida.load_profile()

localhost = load_computer("localhost")
metadata = localhost.metadata.copy()
metadata["default_mpiprocs_per_machine"] = os.cpu_count() // 2
localhost.metadata = metadata
