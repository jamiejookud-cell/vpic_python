import h5py
import os
from code_python.scripts.config.folder_paths import HDF5_OUTPUT_PATH
import code_python.scripts.dumping_backup_python_output as backup

def export_to_hdf5(data_dict, filename):
    """
    Saves a dictionary of numpy arrays into a single HDF5 file.

    Args:
        data_dict: {'name': array, 'name': array, ...}
        filename: name of file (without .h5)
    """

    # Handle human error: forget to create data_dict
    if not isinstance(data_dict, dict):
        data_dict = {'data': data_dict}

    filepath = os.path.join(HDF5_OUTPUT_PATH, f"{filename}.h5")

    with h5py.File(filepath, 'w') as hf:
        for key, array in data_dict.items():
            # compression="gzip" makes the 70MB CSV even smaller (~15-20MB)
            hf.create_dataset(key, data=array, compression="gzip", compression_opts=4)

    backup.dump_process(f"Exported {filepath}")

def import_from_hdf5(filename):
    """
    Loads an HDF5 file and returns a dictionary of arrays.
    """
    filepath = os.path.join(HDF5_OUTPUT_PATH, f"{filename}.h5")
    data_dict = {}

    with h5py.File(filepath, 'r') as hf:
        for key in hf.keys():
            data_dict[key] = hf[key][:]  # [:] loads the data into a numpy array

    backup.dump_process(f"Imported {filename} from {filepath}")

    return data_dict