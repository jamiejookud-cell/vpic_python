from matplotlib.colors import LinearSegmentedColormap

# v16_angle75_mach8: 64584, 142506 ~ 1000 snapshots     v_sh = 0.05609
# v16_angle30_mach8: 120042,  290000 ~ 2000 snapshots
# 87686.0 + 40000
# ---------------------------------- Timestep Setup ---------------------------------- #
TIMESTEP_RANGE: tuple[int, int] = (-1, -1)
SPECIFIC_TIMESTEP: int          = 180492
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
IS_CALCULATING_SHOCK_SPEED: bool            = False
# IS_CALCULATING_SHOCK_VELOCITY:
# Compute shock speed by tracking rho_i vs timestep. Output is the V_SH value and the tracking graph.
# *** NOTE: Be sure not to include T.0 or T.XXXXXX that shock hit the boundary in the TIMESTEP_RANGE. ***

box_frame = [0, 0, 3072, 1024] # [x0, y0, length, height]
IS_CALCULATING_LORENTZ_TRANSFORMATION: bool = False
target_velocity: float = 0.04014

ENABLE_ADVANCED_CALCULATION: bool           = False

IS_EXPORT_DATA_TO_HDF5: bool                = False
# ------------------------------------------------------------------------------------ #


# -------------------------------- Plotting Setup --------------------------------- #
# white to dark-red
wtdr = LinearSegmentedColormap.from_list("wtdr", [(1, 1, 1), (1, .8, .8), (1, .5, .5), (1, 0, 0), (.5, 0, 0)])
# dark-blue to white
dbtw = LinearSegmentedColormap.from_list("dbtw", [(0, 0, .5), (0, 0, 1), (.5, .5, 1), (.8, .8, 1), (1, 1, 1)])

IS_SAVE_FIG: bool = True  # Enable/disable saving figures
# --------------------------------------------------------------------------------- #