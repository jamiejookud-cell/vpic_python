# plot total
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import csv
from code_python.scripts.custom_advanced_function import *

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
folder_path = "C:/Users/nongj/OneDrive/เอกสาร/Globus/prime/electron/momentum_flux"

component = "x"
div_P = import_csv(f"{folder_path}/div_P_{component}")
E_B = import_csv(f"{folder_path}/E_B_{component}")
rho_uu = import_csv(f"{folder_path}/rho_uu_{component}")

# --- PLOT ---
total = -div_P + E_B - rho_uu

div_P = np.mean(div_P, axis=1)
E_B = np.mean(E_B, axis=1)
rho_uu = np.mean(rho_uu, axis=1)
total = np.mean(total, axis=1)

show = True
filename = f"{component}"
fig, ax = plt.subplots(figsize=(8, 4))
plt.title(f"{component}-component", fontsize=12)

ax.plot(-div_P, label='-<divP> term')
ax.plot(E_B, label='<E+uxB> term')
ax.plot(-rho_uu, label='-<rho_uu> term')
ax.plot(total, label='total', color='black')

ax.plot(np.zeros_like(total), '--', color='black')

ax.legend()
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