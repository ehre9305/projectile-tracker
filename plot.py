import matplotlib.pyplot as plt
import numpy as np


def plot(time, x, y, meters_per_pixel):
    # Extracting x and y coordinates from the data
    time = np.array(time) - time[0]
    y = np.array(y) * meters_per_pixel
    x = np.array(x) * meters_per_pixel
    # time = [point[0] for point in points]
    # x = [point[1] for point in points]
    # y = [point[2] for point in points]

    # Creating the scatter plot
    plt.scatter(time, x, label="x")
    plt.scatter(time, y, label="y")

    # Adding labels and title
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("Time vs Value")

    regression_time = np.linspace(0, time[-1], 100)

    # Adding quadratic regression for y
    quadratic_coeffs = np.polyfit(time, y, 2)
    quadratic_func = np.poly1d(quadratic_coeffs)
    quadratic_y = quadratic_func(regression_time)
    plt.plot(regression_time, quadratic_y, label="Quadratic Regression for y")

    # Adding linear regression for x
    linear_coeffs = np.polyfit(time, x, 1)
    linear_func = np.poly1d(linear_coeffs)
    linear_x = linear_func(regression_time)
    plt.plot(regression_time, linear_x, label="Linear Regression for x")

    # Adding quadratic regression for y
    quadratic_coeffs = np.polyfit(time[: int(len(x) / 1.7)], y[: int(len(x) / 1.7)], 2)
    quadratic_func = np.poly1d(quadratic_coeffs)
    quadratic_y = quadratic_func(regression_time)
    plt.plot(
        regression_time, quadratic_y, label="limited data Quadratic Regression for y"
    )

    # Adding linear regression for x
    linear_coeffs = np.polyfit(time[: int(len(x) / 1.7)], x[: int(len(x) / 1.7)], 1)
    linear_func = np.poly1d(linear_coeffs)
    linear_x = linear_func(regression_time)
    plt.plot(regression_time, linear_x, label="limited data Linear Regression for x")

    # Showing the legend
    plt.legend()

    # Displaying the plot
    plt.show()
