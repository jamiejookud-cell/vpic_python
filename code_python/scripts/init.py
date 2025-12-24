FOLDER_PATH      = '/pscratch/sd/k/kittiya/mean_project/vpic2'

# Prepare for dumping files
CODE_FILES_PATH  = f'{FOLDER_PATH}/code_python2/scripts'
FILES_TO_PRINT   = ["init.py", "settings.py", "define.py", "custom_advanced_function.py", "main.py"]
OUTPUT_FILE_PATH = f'{FOLDER_PATH}/code_python2/records'

# CSV files output
CSV_OUTPUT_PATH  = f'{FOLDER_PATH}/code_python2/csv_files'

# Shock dictionary that contains 'hydro_hdf5', 'field_hdf5' and 'info.file'
SHOCK_DATA_PATH  = f'{FOLDER_PATH}/shock_perp75-mach8'

# Output dictionary for saving generated figures
FIG_OUTPUT_PATH  = f'{FOLDER_PATH}/code_python2/images'

# FIXME: manually set parameters
# Dumping info.file
# ------------------------------ Simulation Parameters ------------------------------ #
nx: int = 8192                 # grid cell x
nz: int = 1024                 # grid cell z

dt_wpe: float = 6.363961e-02   # electron time resolution      [time (wpe-1) / time code]
dt_wci: float = 1.272792e-04   # ion cyclotron time resolution [time (wci-1) / time code]

dx_de: float = 1.000000e-01    # length x resolution           [length (de) / length code]
dz_de: float = 1.000000e-01    # length z resolution           [length (de) / length code]

timestep_interval: int = 78
# ------------------------------------------------------------------------------------ #
