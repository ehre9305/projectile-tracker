import numpy as np

import constants


def create_lines(t, x, y):
    y_coeffs = [-4.9] + list(
        np.polyfit(t, [y[i] + 4.9 * t[i] ** 2 for i in range(len(t))], 1)
    )
    y_coeffs_unfixed = list(np.polyfit(t, y, 2))
    x_coeffs = [0] + list(np.polyfit(t, x, 1))

    data = {
        constants.X_FUNC_NAME: (x_coeffs),
        constants.Y_FUNC_NAME: (y_coeffs),
        constants.Y_FUNC_NO_GRAV_NAME: (y_coeffs_unfixed),
    }

    return data


def get_velocity_from_line(coeffs, times):
    func = np.poly1d(coeffs)
    vel_func = func.deriv()

    return vel_func(times)


def get_total_velocity_from_lines(x_coeffs, y_coeffs, times):
    return np.sqrt(
        get_velocity_from_line(x_coeffs, times) ** 2
        + get_velocity_from_line(y_coeffs, times) ** 2
    )


def get_velocity_angles_from_lines(x_coeffs, y_coeffs, times, deg=True):
    out = np.arctan2(
        get_velocity_from_line(x_coeffs, times),
        get_velocity_from_line(y_coeffs, times),
    )

    if deg:
        out = np.rad2deg(out)

    return out


def get_initial_velocity(x_coeffs, y_coeffs):
    return get_total_velocity_from_lines(x_coeffs, y_coeffs, 0)


def predict_last_time_to_cross(coeffs, target):
    func = np.poly1d(coeffs)

    func.coeffs -= target

    return func.roots.max()


def get_camera_angle(t, x, y, deg=True):
    y_func = np.poly1d(np.polyfit(t, y, 2))
    x_func = np.poly1d(np.polyfit(t, x, 2))

    y_accel = y_func.deriv()[1]
    x_accel = x_func.deriv()[1]

    print(y_func)
    print(y_accel)
    print(x_func)
    print(x_accel)

    out = np.arctan2(x_accel, y_accel)

    if deg:
        out = np.rad2deg(out)

    return out
