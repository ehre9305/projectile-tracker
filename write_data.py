import pandas as pd
import numpy as np

POINTS_FILENAME = "points.csv"
COEFFS_FILENAME = "coeffs.csv"


def write_data(data, file, header=False):
    df = pd.DataFrame(data=data)
    df.to_csv(file, header=header, index=False)


def write_points(t, x, y):
    write_data((t, x, y), POINTS_FILENAME)


Y_FUNC_NAME = "y func"
X_FUNC_NAME = "x func"
Y_FUNC_NO_GRAV_NAME = "y func unfixed gravity"


def create_lines(t, x, y):
    y_coeffs = [-4.9] + list(
        np.polyfit(t, [y[i] + 4.9 * t[i] ** 2 for i in range(len(t))], 1)
    )
    y_coeffs_unfixed = list(np.polyfit(t, y, 2))
    x_coeffs = [0] + list(np.polyfit(t, x, 1))

    data = {
        X_FUNC_NAME: (x_coeffs),
        Y_FUNC_NAME: (y_coeffs),
        Y_FUNC_NO_GRAV_NAME: (y_coeffs_unfixed),
    }

    return data


def write_lines(lines):
    write_data(lines, COEFFS_FILENAME, header=True)


def create_limited_lines(t, x, y, points_to_count):
    write_lines(
        create_lines(
            t[:points_to_count],
            x[:points_to_count],
            y[:points_to_count],
        )
    )
