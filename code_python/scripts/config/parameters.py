# ------------------------------ Simulation Parameters ------------------------------ #
nx: int = 8192                 # grid cell x (length code)
nz: int = 1024                 # grid cell z (length code)

dt_wpe: float = 6.363961e-02   # electron time resolution      [time (wpe-1) / time code]
dt_wci: float = 1.272792e-04   # ion cyclotron time resolution [time (wci-1) / time code]

dx_de: float = 1.000000e-01    # length x resolution           [length (de) / length code]
dz_de: float = 1.000000e-01    # length z resolution           [length (de) / length code]

timestep_interval: int = 78    # (time code)
# ------------------------------------------------------------------------------------ #