import numpy as np

import constants

# np.polyfit(x,y,deg) does a regression using the x and y arrays as data points in a regression that results in a polynomial of degree deg
# np.poly1d is a representation of a polynomial

# t, x, and y refer to a lists of time, x positions in meters, and y positions in meters

def create_fixed_y_line(t, y):
    # a as in ax^2 + bx + c
    a = constants.GRAVITY / 2

    # this subtracts the value that the acceleration contributes to the final value
    y_without_accel = [y[i] - a * t[i] ** 2 for i in range(len(t))]

    linear_data = np.polyfit(t, y_without_accel, 1)

    # list of coeffs [a, b, c]
    return [a] + list(linear_data)


def create_lines(t, x, y):
    y_coeffs = create_fixed_y_line(t, y)

    y_coeffs_unfixed = list(np.polyfit(t, y, 2))

    # we are assuming 0 accel and are using a degree 1 regression (linear)
    x_coeffs = [0] + list(np.polyfit(t, x, 1))

    # output dict
    data = {
        constants.X_FUNC_NAME: (x_coeffs),
        constants.Y_FUNC_NAME: (y_coeffs),
        constants.Y_FUNC_NO_GRAV_NAME: (y_coeffs_unfixed),
    }

    return data


def get_velocity_from_line(coeffs, time):
    func = np.poly1d(coeffs) # create a polynomial from input coefficients
    vel_func = func.deriv() # take derivative to get a function for velocity

    return vel_func(time) # returns the value of velocity at the given time


def get_total_velocity_from_lines(x_coeffs, y_coeffs, times):
    # Pythagorean theorem to velocity function above
    return np.sqrt(
        get_velocity_from_line(x_coeffs, times) ** 2
        + get_velocity_from_line(y_coeffs, times) ** 2
    )


def get_velocity_angles_from_lines(x_coeffs, y_coeffs, times, deg=True):
    # arctan2 does arctan and deals with the signs of the x and y
    out = np.arctan2(
        get_velocity_from_line(y_coeffs, times),
        get_velocity_from_line(x_coeffs, times),
    )

    if deg: # convert from radians to degrees by default
        out = np.rad2deg(out)

    return out


def get_initial_velocity(x_coeffs, y_coeffs):
    return get_total_velocity_from_lines(x_coeffs, y_coeffs, 0)


def predict_last_time_to_cross(coeffs, target):
    func = np.poly1d(coeffs)

    func[0] -= target

    if func.roots.size == 0:
        return None

    return func.roots.max()


def get_camera_angle(t, x, y, deg=True):
    y_func = np.poly1d(np.polyfit(t, y, 2))
    x_func = np.poly1d(np.polyfit(t, x, 2))

    y_accel = y_func.deriv().deriv()[0] # accel is the constant term (x^0) of the second derivative of position
    x_accel = x_func.deriv().deriv()[0]

    print(y_func)
    print(y_accel)
    print(x_func)
    print(x_accel)

    out = np.arctan2(x_accel, -y_accel)

    if deg:
        out = np.rad2deg(out)

    return out


def get_scale_meters(y_line):
    gravity = np.poly1d(y_line).deriv()[1] # entry #1 is the x^1 coefficient, which is in case is acceleration
    return constants.GRAVITY / gravity # gravity in meter:gravity in pixels = meters:pixels


def get_distance(meters_per_pixel):
    frame_width_meters = constants.CAMERA_WIDTH * meters_per_pixel

    distance = (frame_width_meters / 2) / np.tan(
        # deg2rad converts degrees to radians (duh)
        np.deg2rad(constants.CAMERA_ANGLE_X / 2)
    )

    return distance


def get_distance_from_line(y_line):
    return get_distance(get_scale_meters(y_line))
