import matplotlib.pyplot as plt
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

    return data
folder_path = "C:/Users/nongj/OneDrive/เอกสาร/Globus/prime/ion/j_e_macro_ratio"

charge = 'e'

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


E = [Ex, Ey, Ez]
B = [Bx, By, Bz]
B2 = Bx * Bx + By * By + Bz * Bz

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

du_dt = [dux_dt + partial_space(ux, 'x') * ux + partial_space(ux, 'z') * uz,
         duy_dt + partial_space(uy, 'x') * ux + partial_space(uy, 'z') * uz,
         duz_dt + partial_space(uz, 'x') * ux + partial_space(uz, 'z') * uz]

term3 = -n * m * cross_product(du_dt, B) / B2  # [term3_x, term3_y, term3_z]