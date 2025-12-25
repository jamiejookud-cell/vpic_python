from matplotlib.colors import LinearSegmentedColormap
# -------------------------------- Plotting Setup --------------------------------- #
# white to dark-red
wtdr = LinearSegmentedColormap.from_list("wtdr", [(1, 1, 1), (1, .8, .8), (1, .5, .5), (1, 0, 0), (.5, 0, 0)])
# dark-blue to white
dbtw = LinearSegmentedColormap.from_list("dbtw", [(0, 0, .5), (0, 0, 1), (.5, .5, 1), (.8, .8, 1), (1, 1, 1)])

IS_SAVE_FIG: bool = True  # Enable/disable saving figures
# --------------------------------------------------------------------------------- #
