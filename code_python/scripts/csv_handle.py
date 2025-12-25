import os
import csv
import numpy as np
from code_python.scripts.config.folder_paths import CSV_OUTPUT_PATH
import code_python.scripts.dumping_backup_python_output as backup

# ---------------------------------------- #
#            export to CSV file            #
# ---------------------------------------- #
def export_csv(data, filename, header=None):
    """
    Export list, 1D numpy array, or 2D numpy array to CSV file.

    Args:
        data: list, 1D np.ndarray, or 2D np.ndarray
        filename: name of file (without .csv)
        header: optional list of column names (only used for 1D or 2D)
    """
    flag = None  # 1 = 1D, 2 = 2D

    if isinstance(data, list):
        # Assume 1D list
        flag = 1
    elif isinstance(data, np.ndarray):
        if data.ndim == 1:
            data = data.tolist()
            flag = 1
        elif data.ndim == 2:
            flag = 2
        else:
            raise ValueError("Only 1D or 2D arrays are supported.")
    else:
        raise TypeError("data must be a list or numpy.ndarray.")

    csv_filepath = os.path.join(CSV_OUTPUT_PATH, f"{filename}.csv")

    with open(csv_filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if header:
            writer.writerow(header)
        if flag == 1:
            writer.writerow(data)
        elif flag == 2:
            writer.writerows(data)

    backup.dump_process(f"Output '{filename}.csv' to {CSV_OUTPUT_PATH}/{filename}.csv")