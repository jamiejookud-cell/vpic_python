import numpy as np
import matplotlib.pyplot as plt
import scipy
from code_python.scripts.config.folder_paths import FIG_OUTPUT_PATH
from code_python.scripts.config.parameters import *
import code_python.scripts.dumping_backup_python_output as backup

shock_distances = []  # [length grid]
shock_times = []      # [time grid]

# ---------------------------------------- #
#         Shock Detection Function         #
# ---------------------------------------- #
def get_shock_peak_index(var_2d_array: np.ndarray) -> float:
    """Return the X index (as float) where the variable peaks (averaged over Z)."""
    var_1d_array = np.mean(var_2d_array, axis=1)
    return float(np.argmax(var_1d_array))

def show_graph_of_shock_speed_tracking():
    # Transform this 'list' to 'np.array', able to use the 'curve_fit' function.
    x_range = np.array(shock_distances)
    t_range = np.array(shock_times)

    # Fitting graph to linear
    def linear(a, x, b):
        return a * x + b

    popt, pcov = scipy.optimize.curve_fit(linear, x_range, t_range)
    t_range_fit = linear(x_range, *popt)

    v_sh_fit = float((x_range[-1]) - float(x_range[0])) / float((t_range_fit[-1]) - float(t_range_fit[0]))
    backup.dump_process(f"Physical V_SH_FIT = {v_sh_fit} [length (de) / time (wpe-1)]")

    plt.title("Peak tracking")
    plt.text(0, 0, f'Physical V_SH_FIT = {v_sh_fit:.05f}', fontsize=8)
    plt.scatter(t_range / dt_wpe, x_range / dx_de, label='peak at each timestep', s=5)
    plt.xlabel("time (code unit)")
    plt.ylabel("x (code unit)")
    plt.plot(t_range_fit / dt_wpe, x_range / dx_de, '--',
             color='orange', label='linear fit line', lw=1)
    plt.legend()
