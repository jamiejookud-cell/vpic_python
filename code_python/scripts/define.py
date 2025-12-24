import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.ticker import FuncFormatter # For adjust unit labels
from scipy import ndimage # Filtering graph
from scipy.optimize import curve_fit # Linear curve fit
from natsort import natsorted # Sort folders
from datetime import datetime # Timestamp output
from init import *
from settings import *

process_txt: str = ""
def dump_process(txt: str):
    global process_txt
    process_txt += "\n" + txt
    print(txt)

X_SIZE: tuple = (0, nx)
Z_SIZE: tuple = (0, nz)
BOX_FRAME: tuple = (x0, y0, length, height)
# ---------------------------------------- #
#             Pre-allocate Data            #
# ---------------------------------------- #
simulation_frame_zero_array = np.zeros((nx, nz))
box_frame_zero_array = np.zeros((length, height))

# hydro electron hdf5 data
jx_e = simulation_frame_zero_array.copy()
jy_e = simulation_frame_zero_array.copy()
jz_e = simulation_frame_zero_array.copy()
ke_e = simulation_frame_zero_array.copy()
px_e = simulation_frame_zero_array.copy()
py_e = simulation_frame_zero_array.copy()
pz_e = simulation_frame_zero_array.copy()
rho_e = simulation_frame_zero_array.copy()
txx_e = simulation_frame_zero_array.copy()
txy_e = simulation_frame_zero_array.copy()
tyy_e = simulation_frame_zero_array.copy()
tyz_e = simulation_frame_zero_array.copy()
tzx_e = simulation_frame_zero_array.copy()
tzz_e = simulation_frame_zero_array.copy()

# hydro ion hdf5 data
jx_i = simulation_frame_zero_array.copy()
jy_i = simulation_frame_zero_array.copy()
jz_i = simulation_frame_zero_array.copy()
ke_i = simulation_frame_zero_array.copy()
px_i = simulation_frame_zero_array.copy()
py_i = simulation_frame_zero_array.copy()
pz_i = simulation_frame_zero_array.copy()
rho_i = simulation_frame_zero_array.copy()
txx_i = simulation_frame_zero_array.copy()
txy_i = simulation_frame_zero_array.copy()
tyy_i = simulation_frame_zero_array.copy()
tyz_i = simulation_frame_zero_array.copy()
tzx_i = simulation_frame_zero_array.copy()
tzz_i = simulation_frame_zero_array.copy()

# electric and magnetic fields hdf5 data
cex = simulation_frame_zero_array.copy()
cey = simulation_frame_zero_array.copy()
cez = simulation_frame_zero_array.copy()
cbx = simulation_frame_zero_array.copy()
cby = simulation_frame_zero_array.copy()
cbz = simulation_frame_zero_array.copy()

# derived data used in Lorentz transformation
rho_i_prime = box_frame_zero_array.copy()
jx_i_prime = box_frame_zero_array.copy()
jy_i_prime = box_frame_zero_array.copy()
jz_i_prime = box_frame_zero_array.copy()

rho_e_prime = box_frame_zero_array.copy()
jx_e_prime = box_frame_zero_array.copy()
jy_e_prime = box_frame_zero_array.copy()
jz_e_prime = box_frame_zero_array.copy()

cex_prime = box_frame_zero_array.copy()
cey_prime = box_frame_zero_array.copy()
cez_prime = box_frame_zero_array.copy()

cbx_prime = box_frame_zero_array.copy()
cby_prime = box_frame_zero_array.copy()
cbz_prime = box_frame_zero_array.copy()

# Shock velocity tracking
shock_distances = []  # [length grid]
shock_times = []      # [time grid]

# ---------------------------------------- #
#         Folder Preprocessing             #
# ---------------------------------------- #
folders = []
_folders = []
__folders = []

# If SPECIFIC_TIMESTEP is applied
if SPECIFIC_TIMESTEP != -1:
    folders = [f"T.{SPECIFIC_TIMESTEP}"]
else:
    # Output example >>> ['T.0', 'T.3100', ...]
    # List all timestep folders from hydro_hdf5/
    __folders = natsorted(os.listdir(f"{SHOCK_DATA_PATH}/hydro_hdf5"))

    # Select based on timestep range
    for f in __folders:
        file_timestep = int(f[2:])
        t_min, t_max = TIMESTEP_RANGE
        if (t_min == -1 and t_max == -1) or \
           (t_min != -1 and t_min <= file_timestep <= t_max) or \
           (t_min == -1 and file_timestep <= t_max) or \
           (t_max == -1 and file_timestep >= t_min):
            _folders.append(f)

    # Apply file skipping
    folders = [f for i, f in enumerate(_folders) if i % SKIP_TO_FOLDER == 0] \
        if SKIP_TO_FOLDER > 1 else _folders
folder_count = len(folders)
dump_process(f"folder count = {folder_count}")

# ---------------------------------------- #
#        HDF5 Data Reader Function         #
# ---------------------------------------- #
# NOTE: Code runs very fast if we import only necessary files
def read_timestep(filename: str) -> dict or None:
    """
    Parameters
    ----------
    filename : str
        Name of the timestep file, e.g. 'T.0', 'T.3100'.

    Returns
    -------
    dict or None
        A dictionary mapping variable names to 2D numpy arrays,
        or None if the file cannot be read.

        //  float jx, jy, jz, rho; // Current and charge density => <q v_i f>, <q f>
        //  float PX, PY, PZ, KE;  // Momentum and K.E. (mass) density  => <p_i f>, <m c^2 (gamma-1) f>
        //  float txx, tyy, tzz;   // Stress diagonal            => <p_i v_j f>, i==j
        //  float tyz, tzx, txy;   // Stress off-diagonal        => <p_i v_j f>, i!=j

        Guide how to find variables from our data

        find number density >>>
        data: rho = <q f> = q * n          # charge density
        -> n = rho / q                     # number density

        find flow velocity >>>
        data: j_i = <q v_i f> = q * (n * u_i)    # current density
        -> u_i = j_i / (q * n)                   # flow velocity

        find momentum >>> (two ways)
        data: P_I = (m * n) * p_i          # momentum (mass) density
        -> p_i = P_I / (m * n)             # momentum

        n * u_i = <gamma v_i f>
        (m * n) * u_i = <gamma m v_i f> = <p_i f> = P_I = (m * n) * p_i
        -> p_i = u_i = j_i / (q * n)       # momentum


        Keys in the dictionary:
            't'      : current timestep

            'jx_e'  : electron current density (x-component)
            'jy_e'  : electron current density (y-component)
            'jz_e'  : electron current density (z-component)
            'ke_e'  :        -
            'px_e'  :        -
            'py_e'  :        -
            'pz_e'  :        -
            'rho_e' : electron charge density
            'txx_e' :        -
            'txy_e' :        -
            'tyy_e' :        -
            'tyz_e' :        -
            'tzx_e' :        -
            'tzz_e' :        -

            'jx_i'  : ion current density (x-component)
            'jy_i'  : ion current density (y-component)
            'jz_i'  : ion current density (z-component)
            'ke_i'  :        -
            'px_i'  :        -
            'py_i'  :        -
            'pz_i'  :        -
            'rho_i' : ion charge density
            'txx_i' :        -
            'txy_i' :        -
            'tyy_i' :        -
            'tyz_i' :        -
            'tzx_i' :        -
            'tzz_i' :        -

            'cex'   : cell-centered electric field (x)
            'cey'   : cell-centered electric field (y)
            'cez'   : cell-centered electric field (z)
            'cbx'   : cell-centered magnetic field (x)
            'cby'   : cell-centered magnetic field (y)
            'cbz'   : cell-centered magnetic field (z)
    """
    current_timestep = int(filename[2:])
    try:
        electron_file_path_location = (f'{SHOCK_DATA_PATH}/hydro_hdf5/T.{current_timestep}'
                                       f'/hydro_electron_{current_timestep}.h5')
        ion_file_path_location = (f'{SHOCK_DATA_PATH}/hydro_hdf5/T.{current_timestep}'
                                  f'/hydro_ion_{current_timestep}.h5')

        # Importing electron file data, subscript with 'e'
        with h5py.File(electron_file_path_location, 'r') as hdf5_r:
            jx_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/jx'][:])
            jy_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/jy'][:])
            jz_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/jz'][:])
            # ke_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/ke'][:])
            # px_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/px'][:])
            # py_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/py'][:])
            # pz_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/pz'][:])
            rho_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/rho'][:])
            # txx_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/txx'][:])
            # txy_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/txy'][:])
            # tyy_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/tyy'][:])
            # tyz_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/tyz'][:])
            # tzx_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/tzx'][:])
            # tzz_e = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/tzz'][:])

        # # Importing ion file data, subscript with 'i'
        # with h5py.File(ion_file_path_location, 'r') as hdf5_r:
        #     jx_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/jx'][:])
        #     jy_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/jy'][:])
        #     jz_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/jz'][:])
        #     ke_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/ke'][:])
        #     px_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/px'][:])
        #     py_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/py'][:])
        #     pz_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/pz'][:])
        #     rho_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/rho'][:])
        #     txx_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/txx'][:])
        #     txy_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/txy'][:])
        #     # tyy_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/tyy'][:])
        #     tyz_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/tyz'][:])
        #     tzx_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/tzx'][:])
        #     tzz_i = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/tzz'][:])

        # Importing field file data
        field_file_path_location = (f'{SHOCK_DATA_PATH}/field_hdf5/T.{current_timestep}'
                                    f'/fields_{current_timestep}.h5')
        with h5py.File(field_file_path_location, 'r') as hdf5_r:
            cex = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/ex'][:])
            cey = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/ey'][:])
            cez = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/ez'][:])
            cbx = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/cbx'][:])
            cby = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/cby'][:])
            cbz = np.squeeze(hdf5_r[f'/Timestep_{current_timestep}/cbz'][:])

        arr_2d_data = {
            't'     : current_timestep,

            'jx_e'  : jx_e,
            'jy_e'  : jy_e,
            'jz_e'  : jz_e,
            'ke_e'  : ke_e,
            'px_e'  : px_e,
            'py_e'  : py_e,
            'pz_e'  : pz_e,
            'rho_e' : rho_e,
            'txx_e' : txx_e,
            'txy_e' : txy_e,
            'tyy_e' : tyy_e,
            'tyz_e' : tyz_e,
            'tzx_e' : tzx_e,
            'tzz_e' : tzz_e,

            'jx_i'  : jx_i,
            'jy_i'  : jy_i,
            'jz_i'  : jz_i,
            'ke_i'  : ke_i,
            'px_i'  : px_i,
            'py_i'  : py_i,
            'pz_i'  : pz_i,
            'rho_i' : rho_i,
            'txx_i' : txx_i,
            'txy_i' : txy_i,
            'tyy_i' : tyy_i,
            'tyz_i' : tyz_i,
            'tzx_i' : tzx_i,
            'tzz_i' : tzz_i,

            'cex'   : cex,
            'cey'   : cey,
            'cez'   : cez,
            'cbx'   : cbx,
            'cby'   : cby,
            'cbz'   : cbz,
        }
        return arr_2d_data
    # File not found
    except OSError or FileNotFoundError:
        return None


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

    dump_process(f"Created new csv file at {csv_filepath}")


# ---------------------------------------- #
#         Shock Detection Function         #
# ---------------------------------------- #
def get_shock_peak_index(var_2d_array: np.ndarray) -> float:
    """Return the X index (as float) where the variable peaks (averaged over Z)."""
    var_1d_array = np.mean(var_2d_array, axis=1)
    return float(np.argmax(var_1d_array))

def calculate_shock_velocity():
    # Transform this 'list' to 'np.array', able to use the 'curve_fit' function.
    x_range = np.array(shock_distances)
    t_range = np.array(shock_times)

    # Fitting graph to linear
    def linear(a, x, b):
        return a * x + b

    popt, pcov = curve_fit(linear, x_range, t_range)
    t_range_fit = linear(x_range, *popt)

    v_sh_fit = float((x_range[-1]) - float(x_range[0])) / float((t_range_fit[-1]) - float(t_range_fit[0]))
    dump_process(f"Physical V_SH_FIT = {v_sh_fit} [length (de) / time (wpe-1)]")

    plt.title("Peak 'rho_i' timestep tracking")
    plt.text(0, 0, f'Physical V_SH_FIT = {v_sh_fit:.05f}', fontsize=8)
    plt.scatter(t_range / dt_wpe, x_range / dx_de, label='peak at each timestep', s=5)
    plt.xlabel("time (code unit)")
    plt.ylabel("x (code unit)")
    plt.plot(t_range_fit / dt_wpe, x_range / dx_de, '--',
             color='orange', label='linear fit line', lw=1)
    plt.legend()

# ---------------------------------------- #
#             Figure Plotting              #
# ---------------------------------------- #
def save_figure(filename: str):
    if IS_SAVE_FIG:
        plt.savefig(f'{FIG_OUTPUT_PATH}/{filename}.png', format='png', dpi=600,
                    bbox_inches='tight', pad_inches=0.2)
        dump_process(f"Saved {FIG_OUTPUT_PATH}/{filename}.png")
    else:
        plt.show()

class PlotFlowFigure:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 1))
        self.cbar: plt.colorbar

    def plot_figure(self, timestep:int, data, vbar: tuple[float, float], cmap: str, title :str = ""):
        if VISUAL_SHOCK_FRAME_VIEW:
            # Shock Frame
            self.ax.set_xlim([0, length])
            self.ax.set_ylim([0, height])
            self.ax.set_xticks(np.linspace(0, length, 5))
            self.ax.set_yticks(np.linspace(0, height, 2))
        else:
            # Simulation Frame
            self.ax.set_xlim(X_SIZE)
            self.ax.set_ylim(Z_SIZE)
            self.ax.set_xticks(np.linspace(X_SIZE[0], X_SIZE[1], 5))
            self.ax.set_yticks(np.linspace(Z_SIZE[0], Z_SIZE[1], 2))

        self.ax.xaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val * 0.01:.02f}"))
        self.ax.yaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val * 0.01:.02f}"))

        # self.ax.set_xlabel('X (code unit)')
        # self.ax.set_ylabel('Z (code unit)')

        timestep = timestep - 64584
        if VISUAL_SHOCK_FRAME_VIEW:
            self.ax.set_title(title + " (Shock frame)", fontsize=10)
        else:
            self.ax.set_title(title + " (Simulation frame)", fontsize=10)
        if TIME_UNIT_OPTION == 0:
            self.ax.text(1, 1.3,f'time: {timestep} (time code)',
                         fontsize=8, ha='right', va='top', transform=self.ax.transAxes)
        elif TIME_UNIT_OPTION == 1:
            self.ax.text(1, 1.3,f'time: {(timestep * dt_wpe):.04f}$\\omega_{{pe}}^{{-1}}$',
                         fontsize=8, ha='right', va='top', transform=self.ax.transAxes)
        elif TIME_UNIT_OPTION == 2:
            self.ax.text(1, 1.3,f'time: {(timestep * dt_wci):.04f}$\\Omega_{{ci}}^{{-1}}$',
                         fontsize=8, ha='right', va='top', transform=self.ax.transAxes)

        # Plot image and store references
        im = self.ax.imshow(data.T, cmap=cmap, vmin=vbar[0], vmax=vbar[1], aspect='auto')
        self.cbar = self.fig.colorbar(im, ax=self.ax)
        self.cbar.set_ticks(np.linspace(vbar[0], vbar[1], 5))

    def clear(self):
        self.cbar.remove()
        plt.cla()

    def plot_line(self, reference_position: float, peak_position: float):
        line_y = np.linspace(0, X_SIZE[1], 2)
        line_x_ref = np.zeros(2) + reference_position
        line_x_peak = np.zeros(2) + peak_position
        self.ax.plot(line_x_ref, line_y, ':', color='black')
        # self.ax.plot(line_x_peak, line_y, color='black') # Disabled line tracking rho_i peak

class PlotOneGraphFigure:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 2))

    def plot(self, timestep: int, data, color: str = 'blue', label: str = "", title=""):
        data = np.array(data)
        if len(data.shape) == 2:
            data = np.mean(data, axis=1)

        self.ax.set_xlim(0, len(data))
        self.ax.set_xticks(np.linspace(0, len(data), 10))
        self.ax.set_xlabel('X (code unit)')

        self.ax.set_title(title)
        if TIME_UNIT_OPTION == 0:
            self.ax.text(1, 1.3,f'time: {timestep} (time code)',
                         fontsize=8, ha='right', va='top', transform=self.ax.transAxes)
        elif TIME_UNIT_OPTION == 1:
            self.ax.text(1, 1.3,f'time: {(timestep * dt_wpe):.04f}$\\omega_{{pe}}^{{-1}}$',
                         fontsize=8, ha='right', va='top', transform=self.ax.transAxes)
        elif TIME_UNIT_OPTION == 2:
            self.ax.text(1, 1.3,f'time: {(timestep * dt_wci):.04f}$\\Omega_{{ci}}^{{-1}}$',
                         fontsize=8, ha='right', va='top', transform=self.ax.transAxes)

        data = ndimage.uniform_filter(data, size=GRAPH_SMOOTH_FILTER)
        self.ax.plot(data, color=color, label=label)

        plt.tight_layout()


class PlotMultipleGraphFigure:
    def __init__(self):
        if ENABLE_PLOT_SIX_GRAPH:
            self.fig, self.axes = plt.subplots(3, 3, width_ratios=[1, 1, 0.001], height_ratios=[1, 1, 1], figsize=(12, 6))
            self.axes[0, 2].axis('off')
            self.axes[1, 2].axis('off')
            self.axes[2, 2].axis('off')
        elif ENABLE_PLOT_THREE_GRAPH:
            self.fig, self.axes = plt.subplots(3, 2, width_ratios = [1, 0.001], height_ratios = [1, 1, 1], figsize=(12, 6))
            self.axes[0, 1].axis('off')
            self.axes[1, 1].axis('off')
            self.axes[2, 1].axis('off')

    def plot(self, ax_index: int or tuple[int, int], data:np.ndarray, color:str = 'blue', label:str = ""):
        if len(data.shape) == 2:
            data = np.mean(data, axis=1)
        data = ndimage.uniform_filter(data, size=GRAPH_SMOOTH_FILTER)
        self.axes[ax_index[0], ax_index[1]].plot(data, color=color, label=label)
        self.axes[ax_index[0], ax_index[1]].set_xlim(data.shape[0])
        self.axes[ax_index[0], ax_index[1]].set_xticks(np.linspace(0, data.shape[0], 5))
        self.axes[ax_index[0], ax_index[1]].set_xlabel("X (code unit)")
        self.axes[ax_index[0], ax_index[1]].set_title(MULTIPLE_GRAPH_TITLE[ax_index[0]][ax_index[1]])

ENABLE_PLOT_FLOW_FIGURE = False
ENABLE_PLOT_ONE_GRAPH = False
ENABLE_PLOT_THREE_GRAPH = False
ENABLE_PLOT_SIX_GRAPH = False
if ENABLE_PLOT_FIGURE == 1:
    ENABLE_PLOT_FLOW_FIGURE = True
    fig1 = PlotFlowFigure()
elif ENABLE_PLOT_FIGURE == 2:
    ENABLE_PLOT_ONE_GRAPH = True
    fig2 = PlotOneGraphFigure()
elif ENABLE_PLOT_FIGURE == 3:
    ENABLE_PLOT_THREE_GRAPH = True
elif ENABLE_PLOT_FIGURE == 4:
    ENABLE_PLOT_SIX_GRAPH = True

# Use gamma = 1 / sqrt(1 - v^2), where c = 1 (normalized units)
GAMMA = (1 - V_SH**2)**(-1/2)

CHANGE_TO_DATA_IN_BOX_FRAME: bool = False
VISUAL_SHOCK_FRAME_VIEW: bool = False
if IS_CALCULATING_LORENTZ_TRANSFORMATION:
    CHANGE_TO_DATA_IN_BOX_FRAME = True
    VISUAL_SHOCK_FRAME_VIEW: bool = True

def dump_files(time_start: str):
    # Add date-time to the output file name
    time_end = datetime.now()
    time_output = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{OUTPUT_FILE_PATH}/run_{time_output}.txt"

    # Format for easier reading
    time_start_str = time_start.strftime("%H:%M:%S")
    time_end_str = time_end.strftime("%H:%M:%S")
    date_str = time_start.strftime("%Y/%m/%d")  # same date for start & end

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(f"Code dump created on {time_start_str} - {time_end_str} {date_str}\n")
        outfile.write("=======================================================================================================================\n\n")

        for filename in FILES_TO_PRINT:
            filepath = os.path.join(CODE_FILES_PATH, filename)
            if os.path.exists(filepath):
                outfile.write(f"\n--- {filename} ---\n\n")
                with open(filepath, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n=======================================================================================================================\n"
                                  "\n"
                                  "\n"
                                  "\n"
                                  "\n"
                                  "\n=======================================================================================================================\n")

            else:
                outfile.write(f"\n--- {filename} (NOT FOUND) ---\n\n")
        # Separator
        outfile.write("Process Log:\n")

        # Process log
        outfile.write(process_txt)

        print(f"Save record to {output_file}")
