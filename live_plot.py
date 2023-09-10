import matplotlib.pyplot as plt
import numpy as np


def time_to_y_pos(t, vi, pi):
    g = 9.8
    return g / 2 * t**2 + vi + pi


class LivePlot:
    def __init__(self):
        plt.ion()
        _, self.ax = plt.subplots()
        plt.xlabel("Time (s)")
        plt.ylabel("Position (m)")
        plt.title("Time vs Position")
        (self.xplot,) = self.ax.plot([], [], "bo", label="x")
        (self.xprediction,) = self.ax.plot([], [], "c", label="x prediction")
        (self.yplot,) = self.ax.plot([], [], "ro", label="y")
        (self.yprediction,) = self.ax.plot([], [], "m", label="y prediction")
        plt.legend()
        plt.show()

    def update(self, t, x, y):
        self.xplot.set_data(t, x)
        self.yplot.set_data(t, y)

        if len(t) > 2:
            self.graph_lines(t, x, y)

        self.__update_plot()

    def graph_lines(self, t, x, y):
        y_coeffs = np.polyfit(t, [y[i] - 4.9 * t[i] ** 2 for i in range(len(t))], 1)
        print(y_coeffs)
        x_coeffs = np.polyfit(t, x, 1)
        print(x_coeffs)

        y_func = np.poly1d([4.9] + list(y_coeffs))
        x_func = np.poly1d(x_coeffs)

        times_to_graph = np.linspace(0, 1, 50)

        y_to_graph = y_func(times_to_graph)
        x_to_graph = x_func(times_to_graph)

        self.yprediction.set_data(times_to_graph, y_to_graph)
        self.xprediction.set_data(times_to_graph, x_to_graph)

    def __update_plot(self):
        self.ax.relim()
        self.ax.autoscale()
        plt.draw()
