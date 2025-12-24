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


CHANGE_TO_DATA_IN_BOX_FRAME: bool = False
VISUAL_SHOCK_FRAME_VIEW: bool = False
if IS_CALCULATING_LORENTZ_TRANSFORMATION:
    CHANGE_TO_DATA_IN_BOX_FRAME = True
    VISUAL_SHOCK_FRAME_VIEW: bool = True