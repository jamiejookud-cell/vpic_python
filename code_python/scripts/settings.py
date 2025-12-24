from matplotlib.colors import LinearSegmentedColormap
# ------------------------------------- #
#      Timestep range configuration     #
# ------------------------------------- #
TIMESTEP_RANGE: tuple[int, int] = (64584, 142506) # 64584 (minimum), 142506
SPECIFIC_TIMESTEP: int          = 64584
SKIP_TO_FOLDER: int             = -1

# TIMESTEP_RANGE:
# Use -1 to indicate 'no limit' on either side.
# Examples:
# (-1, -1)    -> from T.start to T.end
# (-1, 10000) -> from T.start to T.10000
# (10000, -1) -> from T.10000 to T.end

# SPECIFIC_TIMESTEP:
# equivalent to TIMESTEP_RANGE = (SPECIFIC_TIMESTEP, SPECIFIC_TIMESTEP)

# SKIP_TO_FOLDER:
# T.6000 T.6001 T.6002 .... T.6020
# Skip folders up to next index. Use -1 to disable.
# Examples: [T.0, T.100, T.200, T.300, T.400, T.500, ...]
# SKIP_TO_FOLDER = 2
# Output >>> [T.0, T.200, T.400, ...]
# ------------------------------------------------------------------------------------ #


# -------------------------------- Calculating Setup --------------------------------- #
IS_CALCULATING_SHOCK_VELOCITY: bool         = False
V_SH: float                                 = 0.05609 # [length (de) / time (wpe-1)]
x0, y0, length, height                      = -2304, 0, 3072, 1024
IS_CALCULATING_LORENTZ_TRANSFORMATION: bool = True
ENABLE_ADVANCED_CALCULATION: bool           = True
IS_EXPORT_DATA_TO_CSV: bool                 = True

# IS_CALCULATING_SHOCK_VELOCITY:
# Compute shock speed by tracking rho_i vs timestep. Output is the V_SH value and the tracking graph.
# *** NOTE: Be sure not to include T.0 or T.XXXXXX that shock hit the boundary in the TIMESTEP_RANGE. ***

# IS_CALCULATING_LORENTZ_TRANSFORMATION:
# Compute Lorentz transformation of shock's frame (must set V_SH > 0)

# ------------------------------------------------------------------------------------ #


# FIXME: make it easier please!!!
# ---------------------------------- Plotting Setup ---------------------------------- #
# ENABLE_PLOT_FIGURE:
# DISABLE                       : 0
# ENABLE_PLOT_FLOW_FIGURE       : 1
# ENABLE_PLOT_ONE_GRAPH (1x1)   : 2
# ENABLE_PLOT_THREE_GRAPH (3x1) : 3
# ENABLE_PLOT_SIX_GRAPH (3x2)   : 4

# TIME_UNIT_OPTION:
# Time code                : 0
# Plasma frequency time    : 1
# Ion cyclotron time       : 2
# This option works with ENABLE_PLOT_FIGURE = 1 and 2

# FIXME: No space unit setup : need x(d_i)

ENABLE_PLOT_FIGURE: int  = 0
TIME_UNIT_OPTION: int    = 2
GRAPH_SMOOTH_FILTER: int = 0    # Smooth filter data when plotting graph
IS_SAVE_FIG: bool        = True # Enable/disable saving figures

# -------------------------------------------- #
#             Specific Plot Setup              #
# -------------------------------------------- #
########## FLOW PLOTTING SETUP ##########
# Custom colormap for plot.
wtdr = LinearSegmentedColormap.from_list("wtdr", [(1,1,1),(1,.8,.8),(1,.5,.5),(1,0,0),(.5,0,0)])
dbtw = LinearSegmentedColormap.from_list("dbtw", [(0,0,.5),(0,0,1),(.5,.5,1),(.8,.8,1),(1,1,1)])
"""
Usage: Plot multiple flow figures.
Input: FLOW_LIST = list[(variable_name, (vmin, vmax), colormap)]
Examples:
    FLOW_LIST = [
        ('rho_i', (0, 5), wtdr),
        ('jx_i', (-1, 1), "seismic"),
        ('jy_i', (-1, 1), "seismic"),
        ('jz_i', (-1, 1), "seismic"),
    ]
     
Output >>> Plot flow of 'rho_i', 'jx_i', 'jy_i' and 'jz_i' figures of each timestep.
"""
FLOW_LIST = [
    # ('rho_i', (0, 8), wtdr),
    # ('jx_i', (-1, 1), "seismic"),
    # ('jy_i', (-1, 1), "seismic"),
    # ('jz_i', (-1, 1), "seismic"),

    ('rho_i', (0, 8), wtdr),
]

# NOTE: These options work if in Simulation Frame (IS_CALCULATING_LORENTZ_TRANSFORMATION = False)
# Optional - visual moving-box rectangle
VISUAL_MOVING_BOX: bool = True
# Optional - visual reference line and shock's peak line. Suggestion should enable VISUAL_MOVING_BOX too
VISUAL_LINE: bool = False
# Define position line to plot in the box
LINE_RATIO_POSITION: float = 0.75 # 0 to 1


########## ONE-GRAPH-FIGURE SETUP ##########
"""
Usage: Plot many variables up to in a single graph.
Input: ONE_GRAPH_LIST = list[variable_name]
Example:
    ONE_GRAPH_LIST = ["cex", "cey", "cez"]      # Plot electric field components
    ONE_GRAPH_LIST = ["cbx", "cby", "cbz"]      # Plot magnetic field components
    ONE_GRAPH_LIST = ["rho_i", "rho_i_prime"]   # Compare variable and its prime version

NOTE: If the list only contains one variable_name, such as ONE_GRAPH_LIST = ["rho_i"], the plot will automatically
      set title and save_figure name output corresponds to variable_name.
"""
ONE_GRAPH_LIST = [
    # "rho_i"
    # "jx_i", "jx_i_prime",
    # "cex", "cey", "cez",
    # "cbx", "cby", "cbz",
    "ux", "uy", "uz",
]
ONE_GRAPH_FIGURE_FILENAME: str = "u_prime_1d_animation" # Output file name.
# Optional - set title of the figure.
ONE_GRAPH_TITLE: str = "u_prime (electron)"
# Optional - set color correspond to each element of ONE_GRAPH_LIST
ONE_GRAPH_COLOR_LIST: list[str] = ['blue', 'orange', 'green']
# Optional - set y-lim of the graph.
ONE_GRAPH_SET_Y_LIMIT: tuple = (0.0, 0.0)

########## MULTIPLE-GRAPH-FIGURE SETUP ##########
"""
Usage: Compare multiple sets of 3-component variables (e.g., vector fields).
Input: MULTIPLE_GRAPH_LIST = list[list[variable_name]]
Format:
    ==================
    |     Figure     |
    |----------------|
    |   1   |   4    |
    |----------------|
    |   2   |   5    |
    |----------------|
    |   3   |   6    |
    ==================
    MULTIPLE_GRAPH_LIST = [
    (1, ...),
    (2, ...),
    (3, ...),
    (4, ...),
    (5, ...),
    (6, ...),
    ]

Example:
    MULTIPLE_GRAPH_LIST = [
    ("cex",),
    ("cey",),
    ("cez",),
    ("cbx",),
    ("cby",),
    ("cbz",),
    ]
# FIME: Must add comma ',' even though a single plot in each graph. I don't know why
"""
MULTIPLE_GRAPH_LIST = [
    ("ux",),
    ("uy",),
    ("uz",),
]

MULTIPLE_GRAPH_FIGURE_FILENAME: str = "" # Output file name
# Optional - set title of the figure.
MULTIPLE_GRAPH_FIGURE_TITLE: str = "Electric and magnetic fields"  # Title for multi-set comparison
# Optional - set title of each graph.
MULTIPLE_GRAPH_TITLE: list[list[str]] = [
    ["ux_e_prime"],
    ["uy_e_prime"],
    ["uz_e_prime"],
]
# Optional - set color correspond to each cell of each element of MULTIPLE_GRAPH_LIST
MULTIPLE_GRAPH_COLOR_LIST: list[str] = ['blue', 'orange', 'green']
# Optional - set legend correspond to each cell of each element of MULTIPLE_GRAPH_LIST
MULTIPLE_GRAPH_LEGEND_LIST: list[str] = ['-', '-']
# Optional - set horizontal limit of each graph. The element correspond to format. Set (0, 0) to disable.
MULTIPLE_GRAPH_SET_Y_LIMITS: list[list[tuple]] = [
    [(0, 0)],
    [(0, 0)],
    [(0, 0)],
]
# ------------------------------------------------------------------------------------ #
