import numpy as np
import matplotlib.pyplot as plt
import scipy
from code_python.scripts.config.folder_paths import FIG_OUTPUT_PATH
from code_python.scripts.config.parameters import *
import code_python.scripts.dumping_backup_python_output as backup

shock_distances = []  # [code length unit]
shock_times = []      # [code time unit]

# ---------------------------------------- #
#         Shock Detection Function         #
# ---------------------------------------- #
def get_shock_peak_index(var_2d_array: np.ndarray) -> float:
    """Return the X index (as float) where the variable peaks (averaged over Z)."""
    var_1d_array = np.mean(var_2d_array, axis=1)
    return float(np.argmax(var_1d_array))

def show_graph_of_shock_speed_tracking():
    y_data = np.array(shock_distances) # [code length unit]
    x_data = np.array(shock_times) # [code time unit]

    # Fitting graph to linear
    def linear(a, x, b):
        return a * x + b

    popt, pcov = scipy.optimize.curve_fit(linear, x_data, y_data)
    slope_fit, intercept_fit = popt

    x_fit = np.array([x_data[0], x_data[-1]])
    y_fit = linear(slope_fit, x_fit, intercept_fit)

    v_sh_fit = (y_fit[1] - y_fit[0]) / (x_fit[1] - x_fit[0]) * dx_de / dt_wpe # [length (de) / time (wpe-1)]
    backup.dump_process(f"Physical V_SH_FIT = {v_sh_fit} [length (de) / time (wpe-1)]")

    plt.title("Peak tracking")
    plt.text(0, 0, f'Physical V_SH_FIT = {v_sh_fit:.05f}', fontsize=8)

    plt.scatter(x_data, y_data, label='peak at each timestep', s=5)
    plt.xlabel("time (code unit)")
    plt.ylabel("x (code unit)")

    plt.plot(x_fit, y_fit, '--', color='orange', label=f'linear fit line', lw=1)
    plt.legend()