import os
import h5py
import re
import numpy as np

Path = os.path

filepath1: str = "C:/Users/nongj/Documents/Globus_files_transfer/compare_data/field_N1_n256/fields_468.h5"
filepath1 = "C:/Users/nongj/Desktop/Plasma_shock_simulation_backup/my_code/0.2/samples/shock_V16/hydro_hdf5/T.31000/hydro_electron_31000.h5"

class OpenHDF5:
    def __init__(self, hdf5_filepath: Path):
        self.filepath = hdf5_filepath
        txt = str(hdf5_filepath).split('/')[-1]
        match = re.search(r'_(\d+)\.', txt)
        self.timestep = match.group(1)

    def readfile(self):
        with h5py.File(self.filepath, 'r') as f:
            # Top-level groups and datasets
            print("Top-level keys (groups or datasets):")
            for key in f.keys():
                print(f"  - {key}")

            # Recursively print full structure (groups, datasets, attributes)
            def print_structure(name, obj):
                print(f"{name} ({type(obj).__name__})")
                if isinstance(obj, h5py.Dataset):
                    print(f"  shape: {obj.shape}, dtype: {obj.dtype}")
            f.visititems(print_structure)

    def read_dataset(self, key: str, get_data = False):
        with h5py.File(self.filepath, 'r') as f:
            data = f[f"Timestep_{self.timestep}/{key}"]
            print("Shape of dataset:", data.shape)

            # Print a small region (e.g., the first 5x5 values)
            print("Sample data (first 5x5):\n", data[:5, 0, :5])

            if get_data:
                return np.array(data[:, 0, :])


data1 = OpenHDF5(filepath1)
data1.readfile()