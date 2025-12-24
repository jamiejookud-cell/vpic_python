import matplotlib.pyplot as plt
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

folder_path = "C:/Users/nongj/OneDrive/เอกสาร/Globus/prime/ion/drift_motion"


charge = 'i'
component = 'x'
# --- data ---
j = import_csv(f"{folder_path}/j{component}_{charge}")
j_1d = np.mean(j, axis=1)

term1 = import_csv(f"{folder_path}/term1{component}_{charge}")
term1_1d = np.mean(term1, axis=1)

term2 = import_csv(f"{folder_path}/term2{component}_{charge}")
term2_1d = np.mean(term2, axis=1)

term3 = import_csv(f"{folder_path}/term3{component}_{charge}")
term3_1d = np.mean(term3, axis=1)

# ------------

# Plot
show = False
filename = f"j{component}_{charge}"
fig, ax = plt.subplots(figsize=(16, 4))
plt.title(f"j{component}'_{charge} drift motion", fontsize=20)


# --- PLOT HERE ---
ax.plot(j_1d, label=f"j{component}'_{charge}")
ax.plot(term1_1d + term2_1d + term3_1d, label="drift motion")

ax.plot(term1_1d, '--', label="pressure gradient force drift", lw=0.8)
ax.plot(term2_1d, '--', label=rf"$\vec{{E}}\times\vec{{B}}$ drift", lw=0.8)
ax.plot(term3_1d, '--', label="particle inertia drift", lw=0.8, color='black')
ax.legend()
# -----------------

ax.set_xlim([0, 3072])
ax.set_xticks(np.linspace(0, 3072, 5))
ax.set_xlabel(r"$x(d_i)$")
ax.xaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val * 0.01:.02f}"))

ax.legend()
plt.tight_layout()

if show:
    plt.show()
else:
    plt.savefig(f'{folder_path}/{filename}.png', format='png', dpi=600,
                bbox_inches='tight', pad_inches=0.2)
    print(f'Saved to {folder_path}/{filename}.png')