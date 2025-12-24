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
folder_path = "C:/Users/nongj/OneDrive/เอกสาร/Globus/prime/drift_motion_macro"

# Import data
charge = 'i'
component = 'x'

jx = import_csv(f"{folder_path}/jx_{charge}_1000")
jy = import_csv(f"{folder_path}/jy_{charge}_1000")
jz = import_csv(f"{folder_path}/jz_{charge}_1000")


txx = import_csv(f"{folder_path}/txx_{charge}_1000")
txy = import_csv(f"{folder_path}/txy_{charge}_1000")
txz = import_csv(f"{folder_path}/txz_{charge}_1000")
tyz = import_csv(f"{folder_path}/tyz_{charge}_1000")
tzz = import_csv(f"{folder_path}/tzz_{charge}_1000")

Bx = import_csv(f"{folder_path}/bx_1000")
By = import_csv(f"{folder_path}/by_1000")
Bz = import_csv(f"{folder_path}/bz_1000")

Ex = import_csv(f"{folder_path}/ex_1000")
Ey = import_csv(f"{folder_path}/ey_1000")
Ez = import_csv(f"{folder_path}/ez_1000")

rho = import_csv(f"{folder_path}/rho_{charge}_1000")

px = import_csv(f"{folder_path}/px_{charge}_1000")
py = import_csv(f"{folder_path}/py_{charge}_1000")
pz = import_csv(f"{folder_path}/pz_{charge}_1000")

# Calculate
vx = jx / rho
vy = jy / rho
vz = jz / rho

E = np.array([Ex, Ey, Ez])
B = np.array([Bx, By, Bz])
B2 = Bx ** 2 + By ** 2 + Bz ** 2

# term [1] macro
div_P = [partial_space(txx, 'x') + partial_space(txz, 'z'),
         partial_space(txy, 'x') + partial_space(tyz, 'z'),
         partial_space(txz, 'x') + partial_space(tzz, 'z')]

term1 = -1 * cross_product(div_P, B) / B2  # [term1_x, term1_y, term1_z]

# term [2] macro
term2 = rho * cross_product(E, B) / B2  # [term2_x, term2_y, term2_z]

# term [3] macro
q = -1
m = 1
if charge == "i":
    q = 1
    m = 100

# number density: n_s = rho_s / q_s
n = rho / q

# u_s = p_s / (n_s * m_s)
ux = px / (n * m)
uy = py / (n * m)
uz = pz / (n * m)

dux_dt = 0
duy_dt = 0
duz_dt = 0

du_dt = [dux_dt + partial_space(ux, 'x') * vx + partial_space(ux, 'z') * vz,
         duy_dt + partial_space(uy, 'x') * vx + partial_space(uy, 'z') * vz,
         duz_dt + partial_space(uz, 'x') * vx + partial_space(uz, 'z') * vz]

term3 = -n * m * cross_product(du_dt, B) / B2  # [term3_x, term3_y, term3_z]

if component == 'x':
    term1 = term1[0][:-1, :-1]
    term2 = term2[0][:-1, :-1]
    term3 = term3[0][:-1, :-1]
elif component == 'y':
    term1 = term1[1][:-1, :-1]
    term2 = term2[1][:-1, :-1]
    term3 = term3[1][:-1, :-1]
elif component == 'z':
    term1 = term1[2][:-1, :-1]
    term2 = term2[2][:-1, :-1]
    term3 = term3[2][:-1, :-1]

# 1d
term1 = np.mean(term1, axis=1)
term2 = np.mean(term2, axis=1)
term3 = np.mean(term3, axis=1)

jx = np.mean(jx, axis=1)
jy = np.mean(jy, axis=1)
jz = np.mean(jz, axis=1)

# --- PLOT ---

show = False
filename = f"j{component}_{charge}_macro"
fig, ax = plt.subplots(figsize=(16, 4))
plt.title(f"macro j{component}'_{charge} drift motion", fontsize=20)

ax.plot(jx, label=f"j{component}'_{charge}")
ax.plot(term1 + term2 + term3, label="drift motion")

ax.plot(term1, '--', label="pressure gradient force drift", lw=0.8)
ax.plot(term2, '--', label=rf"$\vec{{E}}\times\vec{{B}}$ drift", lw=0.8)
ax.plot(term3, '--', label="particle inertia drift", lw=0.8, color='black')
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