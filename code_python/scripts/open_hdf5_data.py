import h5py
import re
import numpy as np

class OpenHDF5:
    def __init__(self, hdf5_filepath:str):
        self.filepath = hdf5_filepath
        txt = str(hdf5_filepath).split('/')[-1]
        match = re.search(r'_(\d+)\.', txt)
        self.timestep = match.group(1)

    def show_keys(self):
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

    def read_key(self, key: str):
        with h5py.File(self.filepath, 'r') as f:
            data = f[f"Timestep_{self.timestep}/{key}"]
            # print("Shape of dataset:", data.shape)
            # # Print a small region (e.g., the first 5x5 values)
            # print("Sample data (first 5x5):\n", data[:5, 0, :5])
            return np.array(data[:, 0, :])