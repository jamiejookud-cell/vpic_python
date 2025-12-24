"""
NOTE: Please ensure that you have tested all folders by using _check_corrupted_hdf5_folders.py
"""

import numpy as np
import os
import h5py
import natsort # Sort folders
from code_python.scripts.config.folder_paths import SHOCK_DATA_PATH
from code_python.scripts.config.parameters import nx, nz
from code_python.scripts.setup.timestep_setup import  TIMESTEP_RANGE, SPECIFIC_TIMESTEP, SKIP_TO_FOLDER
from code_python.scripts.setup.calculation_setup import box_frame
from code_python.scripts.dumping_backup_python_output import dump_process

# ---------------------------------------- #
#             Pre-allocate Data            #
# ---------------------------------------- #
simulation_frame_zero_array = np.zeros((nx, nz))

# hydro electron hdf5 data
jx_e = simulation_frame_zero_array.copy()
jy_e = simulation_frame_zero_array.copy()
jz_e = simulation_frame_zero_array.copy()
ke_e = simulation_frame_zero_array.copy()
px_e = simulation_frame_zero_array.copy()
py_e = simulation_frame_zero_array.copy()
pz_e = simulation_frame_zero_array.copy()
rho_e = simulation_frame_zero_array.copy()
txx_e = simulation_frame_zero_array.copy()
txy_e = simulation_frame_zero_array.copy()
tyy_e = simulation_frame_zero_array.copy()
tyz_e = simulation_frame_zero_array.copy()
tzx_e = simulation_frame_zero_array.copy()
tzz_e = simulation_frame_zero_array.copy()

# hydro ion hdf5 data
jx_i = simulation_frame_zero_array.copy()
jy_i = simulation_frame_zero_array.copy()
jz_i = simulation_frame_zero_array.copy()
ke_i = simulation_frame_zero_array.copy()
px_i = simulation_frame_zero_array.copy()
py_i = simulation_frame_zero_array.copy()
pz_i = simulation_frame_zero_array.copy()
rho_i = simulation_frame_zero_array.copy()
txx_i = simulation_frame_zero_array.copy()
txy_i = simulation_frame_zero_array.copy()
tyy_i = simulation_frame_zero_array.copy()
tyz_i = simulation_frame_zero_array.copy()
tzx_i = simulation_frame_zero_array.copy()
tzz_i = simulation_frame_zero_array.copy()

# electric and magnetic fields hdf5 data
cex = simulation_frame_zero_array.copy()
cey = simulation_frame_zero_array.copy()
cez = simulation_frame_zero_array.copy()
cbx = simulation_frame_zero_array.copy()
cby = simulation_frame_zero_array.copy()
cbz = simulation_frame_zero_array.copy()

# NOTE: prime is denoted Lorentz frame
# derived data used in Lorentz transformation
box_frame_zero_array = np.zeros((box_frame[2], box_frame[3]))

rho_i_prime = box_frame_zero_array.copy()
jx_i_prime = box_frame_zero_array.copy()
jy_i_prime = box_frame_zero_array.copy()
jz_i_prime = box_frame_zero_array.copy()

rho_e_prime = box_frame_zero_array.copy()
jx_e_prime = box_frame_zero_array.copy()
jy_e_prime = box_frame_zero_array.copy()
jz_e_prime = box_frame_zero_array.copy()

cex_prime = box_frame_zero_array.copy()
cey_prime = box_frame_zero_array.copy()
cez_prime = box_frame_zero_array.copy()

cbx_prime = box_frame_zero_array.copy()
cby_prime = box_frame_zero_array.copy()
cbz_prime = box_frame_zero_array.copy()

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
    __folders = natsort.natsorted(os.listdir(f"{SHOCK_DATA_PATH}/hydro_hdf5"))

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
dump_process(f"folder count = {folder_count}")

# ---------------------------------------- #
#        HDF5 Data Reader Function         #
# ---------------------------------------- #
# NOTE: Code runs very fast if we import only necessary files
def read_timestep(shock_folder: str) -> dict:
    """
    continuity equation and energy-momentum tensor
    //  float jx, jy, jz, rho; // Current and charge density => <q v_i f>, <q f>
    //  float px, py, pz, ke;  // Momentum and K.E. density  => <p_i f>, <m c^2 (gamma-1) f>
    //  float txx, tyy, tzz;   // Stress diagonal            => <p_i v_j f>, i==j
    //  float tyz, tzx, txy;   // Stress off-diagonal        => <p_i v_j f>, i!=j
    """
    current_timestep = int(shock_folder[2:])

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

    hdf5_data_set = {
        't'     : current_timestep,

        'jx_e'  : jx_e,
        'jy_e'  : jy_e,
        'jz_e'  : jz_e,
        'ke_e'  : ke_e,
        'px_e'  : px_e,
        'py_e'  : py_e,
        'pz_e'  : pz_e,
        'rho_e' : rho_e,
        'txx_e' : txx_e,
        'txy_e' : txy_e,
        'tyy_e' : tyy_e,
        'tyz_e' : tyz_e,
        'tzx_e' : tzx_e,
        'tzz_e' : tzz_e,

        'jx_i'  : jx_i,
        'jy_i'  : jy_i,
        'jz_i'  : jz_i,
        'ke_i'  : ke_i,
        'px_i'  : px_i,
        'py_i'  : py_i,
        'pz_i'  : pz_i,
        'rho_i' : rho_i,
        'txx_i' : txx_i,
        'txy_i' : txy_i,
        'tyy_i' : tyy_i,
        'tyz_i' : tyz_i,
        'tzx_i' : tzx_i,
        'tzz_i' : tzz_i,

        'cex'   : cex,
        'cey'   : cey,
        'cez'   : cez,
        'cbx'   : cbx,
        'cby'   : cby,
        'cbz'   : cbz,
    }

    return hdf5_data_set