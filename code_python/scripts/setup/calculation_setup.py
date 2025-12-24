# CONST
V_SH: float = 0.05609 # [length (de) / time (wpe-1)]
# This 0.05609 is the speed of shock moving from right to left.

# -------------------------------- Calculating Setup --------------------------------- #
IS_CALCULATING_SHOCK_SPEED: bool            = False
# IS_CALCULATING_SHOCK_VELOCITY:
# Compute shock speed by tracking rho_i vs timestep. Output is the V_SH value and the tracking graph.
# *** NOTE: Be sure not to include T.0 or T.XXXXXX that shock hit the boundary in the TIMESTEP_RANGE. ***

box_frame = [-2304, 0, 3072, 1024] # [x0, y0, length, height]
IS_CALCULATING_LORENTZ_TRANSFORMATION: bool = True
target_velocity: float = V_SH

ENABLE_ADVANCED_CALCULATION: bool           = True

IS_EXPORT_DATA_TO_CSV: bool                 = True
# ------------------------------------------------------------------------------------ #