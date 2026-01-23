import numpy as np

def cross_product(a:list[np.ndarray], b:list[np.ndarray], component:str=""):
    """
    args:
        a: [ax, ay, az]
        b: [bx, by, bz]
        *component: return in component form: 'x', 'y', 'z'
    """
    ax, ay, az, bx, by, bz = a[0], a[1], a[2], b[0], b[1], b[2]

    if component == "x":
        return ay * bz - az * by
    elif component == "y":
        return az * bx - ax * bz
    elif component == "z":
        return ax * by - ay * bx

    cx = ay * bz - az * by
    cy = az * bx - ax * bz
    cz = ax * by - ay * bx
    return np.array([cx, cy, cz])

def partial(arr_2d: np.ndarray, component: str = ""):
    # calculate using centered-grid difference
    # [1:-1, 1:-1]
    dx = 0.1

    if component == "x":
        # A_plus = A(x + dx)
        A_plus = np.roll(arr_2d, -1, axis=0) # (x, z) -> (x+1, z)
        # A_minus = A(x - dx)
        A_minus = np.roll(arr_2d, 1, axis=0) # (x, z)   -> (x-1, z)

        # Centered difference: (A(x+dx) - A(x-dx)) / (2*dx)
        return (A_plus - A_minus) / (2 * dx)

    elif component == "z":
        # A_plus = A(z + dz)
        A_plus = np.roll(arr_2d, -1, axis=1) # (x, z) -> (x, z+1)
        # A_minus = A(z - dz)
        A_minus = np.roll(arr_2d, 1, axis=1) # (x, z) -> (x, z-1)

        # Centered difference: (A(z+dz) - A(z-dz)) / (2*dz)
        return (A_plus - A_minus) / (2 * dx)  # assuming dz = dx = 0.1

    return np.zeros_like(arr_2d)

    # NOTE: With centered difference, you have errors at BOTH boundaries (first and last elements).
    # If you are still using roll, your valid region becomes :-2 and 1:-1 depending on your trimming needs.
    # For simplicity, if you stick to the :-1 trimming, the centered difference error will still be much smaller.

def lorentz_transformation_tensor(ux:np.ndarray, uy:np.ndarray, uz:np.ndarray):

    # gamma_u = (1-u.u/c^2)^-1/2
    uu = ux ** 2 + uy ** 2 + uz ** 2 # u.u = u^2
    gamma_u = (1 - uu) ** -0.5

    # arbitrary velocity
    m00 = gamma_u
    m11 = 1 + (gamma_u - 1) * ux * ux / uu
    m22 = 1 + (gamma_u - 1) * uy * uy / uu
    m33 = 1 + (gamma_u - 1) * uz * uz / uu
    m01 = -gamma_u * ux
    m02 = -gamma_u * uy
    m03 = -gamma_u * uz
    m12 = (gamma_u - 1) * ux * uy / uu
    m13 = (gamma_u - 1) * uy * uz / uu
    m23 = (gamma_u - 1) * uy * uz / uu

    # symmetric matrix: M = M.transpose()
    return np.array([
        [m00, m01, m02, m03],
        [m01, m11, m12, m13],
        [m02, m12, m22, m23],
        [m03, m13, m23, m33],
    ])