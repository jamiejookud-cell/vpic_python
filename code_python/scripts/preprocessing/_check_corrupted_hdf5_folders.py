# run this file to check if there's a corrupted folder in hdf5.
import numpy as np
import os
import h5py
from natsort import natsorted # Sort folders
from code_python.scripts.config.folder_paths import SHOCK_DATA_PATH
from code_python.scripts.config.setup import TIMESTEP_RANGE, SPECIFIC_TIMESTEP, SKIP_TO_FOLDER
# ---------------------------------------- #
#         Folder Preprocessing             #
# ---------------------------------------- #
folders = []
_folders = []
__folders = []

# If SPECIFIC_TIMESTEP is applied
if SPECIFIC_TIMESTEP != -1:
    folders = [f"T.{SPECIFIC_TIMESTEP}"]
else:
    # Output example >>> ['T.0', 'T.3100', ...]
    # List all timestep folders from hydro_hdf5/
    __folders = natsorted(os.listdir(f"{SHOCK_DATA_PATH}/hydro_hdf5"))

    # Select based on timestep range
    for f in __folders:
        file_timestep = int(f[2:])
        t_min, t_max = TIMESTEP_RANGE
        if (t_min == -1 and t_max == -1) or \
           (t_min != -1 and t_min <= file_timestep <= t_max) or \
           (t_min == -1 and file_timestep <= t_max) or \
           (t_max == -1 and file_timestep >= t_min):
            _folders.append(f)

    # Apply file skipping
    folders = [f for i, f in enumerate(_folders) if i % SKIP_TO_FOLDER == 0] \
        if SKIP_TO_FOLDER > 1 else _folders
folder_count = len(folders)

# ---------------------------------------- #
#        HDF5 Data Reader Function         #
# ---------------------------------------- #
def read_timestep(shock_folder: str):
    current_timestep = int(shock_folder[2:])
    try:
        electron_file_path_location = (f'{SHOCK_DATA_PATH}/hydro_hdf5/T.{current_timestep}'
                                       f'/hydro_electron_{current_timestep}.h5')
        ion_file_path_location = (f'{SHOCK_DATA_PATH}/hydro_hdf5/T.{current_timestep}'
                                  f'/hydro_ion_{current_timestep}.h5')

        # Importing electron file data, subscript with 'e'
        with h5py.File(electron_file_path_location, 'r') as hdf5_r:
            jx_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/jx'][:])
            jy_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/jy'][:])
            jz_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/jz'][:])
            ke_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/ke'][:])
            px_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/px'][:])
            py_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/py'][:])
            pz_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/pz'][:])
            rho_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/rho'][:])
            txx_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/txx'][:])
            txy_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/txy'][:])
            tyy_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/tyy'][:])
            tyz_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/tyz'][:])
            tzx_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/tzx'][:])
            tzz_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/tzz'][:])

        # Importing ion file data, subscript with 'i'
        with h5py.File(ion_file_path_location, 'r') as hdf5_r:
            jx_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/jx'][:])
            jy_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/jy'][:])
            jz_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/jz'][:])
            ke_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/ke'][:])
            px_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/px'][:])
            py_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/py'][:])
            pz_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/pz'][:])
            rho_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/rho'][:])
            txx_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/txx'][:])
            txy_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/txy'][:])
            tyy_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/tyy'][:])
            tyz_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/tyz'][:])
            tzx_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/tzx'][:])
            tzz_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/tzz'][:])

        # Importing field file data
        field_file_path_location = (f'{SHOCK_DATA_PATH}/field_hdf5/T.{current_timestep}'
                                    f'/fields_{current_timestep}.h5')
        with h5py.File(field_file_path_location, 'r') as hdf5_r:
            cex = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/ex'][:])
            cey = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/ey'][:])
            cez = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/ez'][:])
            cbx = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/cbx'][:])
            cby = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/cby'][:])
            cbz = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/cbz'][:])

    # File not found or corrupted
    except FileNotFoundError or OSError:
        return False

    return True

corrupted_folders = []
for folder_index, folder_name in enumerate(folders):
    test = read_timestep(shock_folder=folder_name)
    if test:
        print(f"Passed {folder_name}")
    else:
        corrupted_folders.append(folder_name)
        print(f"!!! Found corrupted folder {folder_name} !!!")

print("Corrupted folders:")
print(corrupted_folders)