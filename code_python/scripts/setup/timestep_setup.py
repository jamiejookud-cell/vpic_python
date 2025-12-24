# ------------------------------------- #
#      Timestep range configuration     #
# ------------------------------------- #
TIMESTEP_RANGE: tuple[int, int] = (64584, 142506) # 64584 (time that shock reaches steady state), 142506 (maximum snapshot)
SPECIFIC_TIMESTEP: int          = -1
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