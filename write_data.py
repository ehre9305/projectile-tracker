import pandas as pd

import constants
import analysis


def write_data(data, file, header=False):
    df = pd.DataFrame(data=data)
    df.to_csv(file, header=header, index=False)


def write_points(t, x, y):
    write_data((t, x, y), constants.POINTS_FILENAME)


def write_lines(lines):
    write_data(lines, constants.COEFFS_FILENAME, header=True)


def create_limited_lines(t, x, y, points_to_count):
    if points_to_count > 1:
        write_lines(
            analysis.create_lines(
                t[:points_to_count],
                x[:points_to_count],
                y[:points_to_count],
            )
        )
