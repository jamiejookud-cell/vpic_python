import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter # For adjust unit labels
from code_python.scripts.config.folder_paths import FIG_OUTPUT_PATH
from code_python.scripts.config.parameters import dx_de, dt_wpe, dt_wci
from code_python.scripts.config.setup import *
import code_python.scripts.dumping_backup_python_output as backup

def save_figure(filename: str):
    if IS_SAVE_FIG:
        plt.savefig(f'{FIG_OUTPUT_PATH}/{filename}.png', format='png', dpi=600,
                    bbox_inches='tight', pad_inches=0.2)
        backup.dump_process(f"Saved {FIG_OUTPUT_PATH}/{filename}.png")
        plt.close()
    else:
        plt.show()

# ---------------------------------------- #
#            Built-in plotting             #
# ---------------------------------------- #
class PlotFlowFigure:
    def __init__(self, timestep, data: np.ndarray, vbar: tuple[float, float], cmap: str, units:str ="", disable_time_start_correction=False):
        self.start_timestep = TIMESTEP_RANGE[0]
        self.data = data
        if disable_time_start_correction:
            self.start_timestep = 0
        self.timestep = timestep - self.start_timestep
        self.fig, self.ax = plt.subplots(figsize=(10, 1))
        self.cbar: plt.colorbar

        x_max, y_max = data.shape
        self.ax.set_xlim((0, x_max))
        self.ax.set_ylim((0, y_max))
        self.ax.set_xticks(np.linspace(0, x_max, 5))
        self.ax.set_yticks(np.linspace(0, y_max, 2))
        self.ax.set_xlabel('X (code unit)')
        self.ax.set_ylabel('Z (code unit)')


        # Set units
        units = units.split(" ")
        for unit in units:
            if unit == "de":
                self.ax.xaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val * 0.1:.02f}")) # set x_de
                self.ax.yaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val * 0.1:.02f}")) # set y_de
                self.ax.set_xlabel('X (de)')
                self.ax.set_ylabel('Z (de)')
            elif unit == "di":
                self.ax.xaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val * 0.01:.02f}")) # set x_di
                self.ax.yaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val * 0.01:.02f}")) # set y_di
                self.ax.set_xlabel('X (di)')
                self.ax.set_ylabel('Z (di)')
            elif unit == "wpe":
                self.ax.text(1, 1.3,f'time: {(self.timestep * dt_wpe):.04f}$\\omega_{{pe}}^{{-1}}$',
                             fontsize=8, ha='right', va='top', transform=self.ax.transAxes)
            elif unit == "wci":
                self.ax.text(1, 1.3,f'time: {(self.timestep * dt_wci):.04f}$\\Omega_{{ci}}^{{-1}}$',
                             fontsize=8, ha='right', va='top', transform=self.ax.transAxes)
            else:
                self.ax.text(1, 1.3, f'time: {self.timestep} (time code)',
                             fontsize=8, ha='right', va='top', transform=self.ax.transAxes)

        # Plot image and store references
        im = self.ax.imshow(data.T, cmap=cmap, vmin=vbar[0], vmax=vbar[1], aspect='auto')
        self.cbar = self.fig.colorbar(im, ax=self.ax)
        self.cbar.set_ticks(np.linspace(vbar[0], vbar[1], 5))

    def show_lorentz_frame(self, line_reference_ratio: float = 0):
        """
        Args:
            line_reference_ratio: value between 0 - 1
        """
        self._draw_box_frame()
        self._draw_line_reference_position(line_reference_ratio)

    def _draw_box_frame(self):
        v = target_velocity
        x0, y0, length, height = box_frame
        x_step = int(v * (1 / dx_de) * dt_wpe * (self.timestep + self.start_timestep))

        self.ax.add_patch(Rectangle((x0 + x_step, y0), length, height, linewidth=4, edgecolor='black', facecolor='none'))

    def _draw_line_reference_position(self, reference_position_ratio: float):
        v = target_velocity
        x0, y0, length, height = box_frame
        x_step = int(v * (1 / dx_de) * dt_wpe * (self.timestep + self.start_timestep))

        x = np.zeros(2) + length * reference_position_ratio
        y = np.linspace(0, height, 2)
        self.ax.plot(x0 + x + x_step, y0 + y, ':', color='black')

    def draw_line_peak_position(self):
        y_max = self.data.shape[1]

        peak_position = float(np.argmax(np.mean(self.data, axis=1)))
        x_peak = np.zeros(2) + peak_position
        y = np.linspace(0, y_max, 2)
        self.ax.plot(x_peak, y, color='black')

    @staticmethod
    def show():
        plt.show()

    @staticmethod
    def save(filename: str):
        save_figure(filename)

    def title(self, title: str):
        self.ax.set_title(title)