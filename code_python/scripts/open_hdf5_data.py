import h5py
import re
import numpy as np
import matplotlib.pyplot as plt

class OpenHDF5:
    def __init__(self, hdf5_filepath:str):
        self.filepath = hdf5_filepath
        txt = str(hdf5_filepath).split('/')[-1]
        match = re.search(r'_(\d+)\.', txt)
        self.timestep = match.group(1)

    def show_keys(self):
        with h5py.File(self.filepath, 'r') as f:
            # Top-level groups and datasets
            print("Top-level keys (groups or datasets):")
            for key in f.keys():
                print(f"  - {key}")

            # Recursively print full structure (groups, datasets, attributes)
            def print_structure(name, obj):
                print(f"{name} ({type(obj).__name__})")
                if isinstance(obj, h5py.Dataset):
                    print(f"  shape: {obj.shape}, dtype: {obj.dtype}")
            f.visititems(print_structure)

    def read_key(self, key: str):
        with h5py.File(self.filepath, 'r') as f:
            data = f[f"Timestep_{self.timestep}/{key}"]
            # print("Shape of dataset:", data.shape)
            # # Print a small region (e.g., the first 5x5 values)
            # print("Sample data (first 5x5):\n", data[:5, 0, :5])
            return np.array(data[:, 0, :])

filepath1  = "C:/DEV/python/vpic_python/sample_data/V16/hydro_hdf5/T.64584/hydro_electron_64584.h5"

obj = OpenHDF5(filepath1)
obj.keys()
jx = obj.read("jx")

def pressure_tensor(mass, charge, txx, txy, txz, tyy, tyz, tzz, velocity) -> np.ndarray:
    ...
    return pxx, pxy, pxz, pyy, pyz, pzz

pxx, pxy, pxz, pyy, pyz, pzz = pressure_tensor(100, 1, txx, ...., -0.16)
plt.

# data = OpenHDF5(filepath1)
# c = 1
# m = 100
# q = 1
# rho = data.read('rho')
#
# n = rho / q
# rho_m = m * n
#
# ke = data.read('ke') # K.E density
#
# T00 = m * c ** 2 / n + ke # Total energy density
# T01 = data.read('px') # momentum density
# T02 = data.read('py') # momentum density
# T03 = data.read('pz') # momentum density
# T11 = data.read('txx')
# T22 = data.read('tyy')
# T33 = data.read('tzz')
# T12 = data.read('txy')
# T13 = data.read('tzx')
# T23 = data.read('tyz')
#
# jx = data.read('jx')
# jy = data.read('jy')
# jz = data.read('jz')
#
# ux = jx / rho
# uy = jy / rho
# uz = jz / rho
#
# v = -0.16
# GAMMA = (1 - v ** 2) ** (-1 / 2)
#
# rho_i_prime = GAMMA * (rho - v * jx)
# jx_i_prime = GAMMA * (jx - rho * v)
#
# ux_prime = jx_i_prime / rho_i_prime
#
# # For plot 2d
# data = ux_prime
# cmap = "seismic"
# vbar = [-2, 2]
#
# fig, ax = plt.subplots(figsize=(10, 1))
# im = ax.imshow(data.T, cmap=cmap, vmin=vbar[0], vmax=vbar[1], aspect='auto')
# cbar = fig.colorbar(im, ax=ax)
# cbar.set_ticks(np.linspace(vbar[0], vbar[1], 3))
#
# plt.show()
# # T = np.zeros([4,4,8192,1024])
# # T[0,0] = T00
# # T[0,1] = T01
# # T[0,2] = T02
# # T[0,3] = T03
# # T[1,0] = T01
# # T[1,1] = T11
# # T[1,2] = T12
# # T[1,3] = T13
# # T[2,0] = T02
# # T[2,1] = T12
# # T[2,2] = T22
# # T[2,3] = T23
# # T[3,0] = T03
# # T[3,1] = T13
# # T[3,2] = T23
# # T[3,3] = T33
# #
# # M = lorentz_transformation_tensor(ux, uy, uz)
# #
# # # # ------------------------------------------------ #
# # # # Test just doing T_prime of (X,Z) = (4096, 512)
# # # ux = ux[4096, 512]
# # # uy = uy[4096, 512]
# # # uz = uz[4096, 512]
# # # rho_m = rho_m[4096, 512]
# # #
# # # txx = T11[4096, 512]
# # # tyy = T22[4096, 512]
# # # tzz = T33[4096, 512]
# # #
# # # pxx = txx - rho_m * ux ** 2
# # # pyy = tyy - rho_m * uy ** 2
# # # pzz = tzz - rho_m * uz ** 2
# # #
# # # print(txx)
# # # print(tyy)
# # # print(tzz)
# # # # >>>
# # # # 0.037407674
# # # # 0.011219831
# # # # 0.010335375
# # # print('---')
# # # print(pxx)
# # # print(pyy)
# # # print(pzz)
# # # # >>>
# # # # 0.013237672
# # # # 0.0112143215
# # # # 0.010256909
# #
# # # M = np.matrix(M[:, :, 4096, 512])
# # # >>> M =
# # # [[ 1.0121981  0.1563967  0.0023613 -0.0089111]
# # #  [ 0.1563967  1.0121559  0.0001835 -0.0000105]
# # #  [ 0.0023613  0.0001835  1.0000027 -0.0000105]
# # #  [-0.0089111 -0.0000105 -0.0000105  1.0000395]]
# #
# # # T = np.matrix(T[:, :, 4096, 512])
# # # >>>
# # # [[ 1.0178832 -0.1629214 -0.0024332  0.0095559]
# # #  [-0.1629214  0.0374077  0.000365  -0.0027089]
# # #  [-0.0024332  0.000365   0.0112198  0.0000606]
# # #  [ 0.0095559 -0.0027089  0.0000606  0.0103354]]
# # T_prime = M * T * M
# # print(T_prime)
# # # >>>
# # # [[ 0.9920244 -0.0038308 -0.0000366  0.0002057]
# # #  [-0.0038308  0.0116398 -0.0000203 -0.0011967]
# # #  [-0.0000366 -0.0000203  0.0112141  0.000083 ]
# # #  [ 0.0002057 -0.0011967  0.000083   0.0102467]]
# # # ------------------------------------------------ #
# #
# # #
# # # gamma_u = (1 - ux ** 2 + uy ** 2 + uz ** 2) ** (-0.5)
# # # # 4-velocity
# # # U4 = np.zeros([4, 8192, 1024])
# # # U4[0] = gamma_u * c
# # # U4[1] = gamma_u * ux
# # # U4[2] = gamma_u * uy
# # # U4[3] = gamma_u * uz
# # #
# # # # # test (4096, 512)
# # # # M = M[:, :, 4096, 512]
# # # # ux = ux[4096, 512]
# # # # uy = uy[4096, 512]
# # # # uz = uz[4096, 512]
# # # #
# # # # print(M)
# # # # gamma_u = (1 - ux ** 2 + uy ** 2 + uz ** 2) ** (-0.5)
# # # # print(gamma_u)
# # #
# # # # V'1 = M10V0 + M11V1 + M12V2 + M13V3
# # #
# # # U4_prime = np.einsum('mrXZ, rXZ -> mXZ', M, U4, optimize=True)
# # # ux_prime = U4_prime[1] # U'^{1}
# # # uy_prime = U4_prime[2] # U'^{2}
# # # uz_prime = U4_prime[3] # U'^{3}
# # #
# # # uu_prime = ux_prime ** 2 + uy_prime ** 2 + uz_prime ** 2
# # #
# # # # For plot 2d
# # # data = ux_prime
# # # cmap = "seismic"
# # # vbar = [-0.01, 0.01]
# # # fig, ax = plt.subplots(figsize=(10, 1))
# # # im = ax.imshow(data.T, cmap=cmap, vmin=vbar[0], vmax=vbar[1], aspect='auto')
# # # cbar = fig.colorbar(im, ax=ax)
# # # cbar.set_ticks(np.linspace(vbar[0], vbar[1], 3))
# # #
# # # ax.set_xlim([0, 8192])
# # # ax.set_ylim([0, 1024])
# # # ax.set_xticks(np.linspace(0, 3072, 5))
# # # ax.set_yticks(np.linspace(0, 1024, 2))
# # #
# # # ax.xaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val * 0.01:.02f}"))
# # # ax.yaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val * 0.01:.02f}"))
# # #
# # # plt.show()
# # #
# # # Tensor calculation
# # # T_prime[m, n, X, Z] = M[m, r, X, Z] * T[r, s, X, Z] * M[n, s, X, Z]
# # T_prime = np.einsum('mrXZ, rsXZ, nsXZ -> mnXZ', M, T, M, optimize=True)
# # T11_prime = T_prime[1, 1]
# # T22_prime = T_prime[2, 2]
# # T33_prime = T_prime[3, 3]
# #
# # plt.plot(one(T11_prime), label='T11_prime')
# # plt.plot(one(T22_prime), label='T22_prime')
# # plt.plot(one(T33_prime), label='T33_prime')
# # # # plt.plot(one(T11), label='T11')
# # # # plt.plot(one(T22), label='T22')
# # # # plt.plot(one(T33), label='T33')
# # plt.legend()
# # plt.show()