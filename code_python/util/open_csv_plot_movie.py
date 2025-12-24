import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter
import csv
import numpy as np

def import_csv(csv_filepath, return_mean=False):
    """
    Import CSV file as list or numpy array.

    Args:
        csv_filepath: csv file path (without .csv)
        return_mean: return numpy.mean()

    Returns:
        data: list or numpy array
    """

    with open(f"{csv_filepath}.csv", 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]

    # Convert strings -> float if possible
    def try_convert(x):
        try:
            return float(x)
        except ValueError:
            return x

    rows = [[try_convert(x) for x in row] for row in rows]

    # If only one row -> return 1D
    if len(rows) == 1:
        data = rows[0]
    else:
        data = rows

    if return_mean:
        return np.mean(data)

    return np.array(data)

folder_path = "C:/Users/nongj/OneDrive/เอกสาร/Globus/prime/electron/rho_and_b_movie"

for N in [5, 10, 20, 50, 100, 200, 500, 1000]:
    bx = import_csv(f"{folder_path}/bx_movie_{N}")
    # by = import_csv(f"{folder_path}/by_movie_{N}")
    # bz = import_csv(f"{folder_path}/bz_movie_{N}")
    # rho_e = import_csv(f"{folder_path}/rho_movie_{N}")

    # dbtw = LinearSegmentedColormap.from_list("dbtw", [(0, 0, .5), (0, 0, 1), (.5, .5, 1), (.8, .8, 1), (1, 1, 1)])

    # For plot 2d
    data = bx
    cmap = "seismic"
    vbar = [-2, 2]
    filename = f'bx_{N}'

    fig, ax = plt.subplots(figsize=(10, 1))
    im = ax.imshow(data.T, cmap=cmap, vmin=vbar[0], vmax=vbar[1], aspect='auto')
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_ticks(np.linspace(vbar[0], vbar[1], 3))

    ax.set_xlim([0, 3072])
    ax.set_ylim([0, 1024])
    ax.set_xticks(np.linspace(0, 3072, 5))
    ax.set_yticks(np.linspace(0, 1024, 2))

    ax.xaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val * 0.01:.02f}"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val * 0.01:.02f}"))

    plt.title(f'bx in shock\'s frame (average {N} snapshots)',fontsize=8)
    plt.savefig(f'{folder_path}/{filename}.png', format='png', dpi=600,
                bbox_inches='tight', pad_inches=0.2)
    print(f'Saved to {folder_path}/{filename}.png')