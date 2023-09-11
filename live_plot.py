import matplotlib.pyplot as plt
import numpy as np

# import pyqtgraph as pg


def time_to_y_pos(t, vi, pi):
    g = 9.8
    return g / 2 * t**2 + vi + pi


class LivePlot:
    def __init__(self):
        # self.plog = pg.plot(name="position")
        plt.ion()
        self.fig, self.ax = plt.subplots()
        plt.xlabel("Time (s)")
        plt.ylabel("Position (m)")
        plt.title("Time vs Position")
        (self.xplot,) = self.ax.plot([], [], "bo", label="x")
        (self.xprediction,) = self.ax.plot([], [], "c", label="x prediction")
        (self.yplot,) = self.ax.plot([], [], "ro", label="y")
        (self.yprediction,) = self.ax.plot([], [], "m", label="y prediction")
        plt.legend()

    def start(self, t, x, y):
        self.t = t
        self.x = x
        self.y = y

    def update(self):
        self.xplot.set_data(self.t, self.x)
        self.yplot.set_data(self.t, self.y)

        if len(self.t) > 2:
            self.graph_lines()

        self.__update_plot()

    def graph_lines(self):
        y_coeffs = np.polyfit(
            self.t, [self.y[i] - 4.9 * self.t[i] ** 2 for i in range(len(self.t))], 1
        )
        print(y_coeffs)
        x_coeffs = np.polyfit(self.t, self.x, 1)
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
