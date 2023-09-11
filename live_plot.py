import numpy as np
import pyqtgraph as pg
import pyqtgraph.multiprocess as mp


def time_to_y_pos(t, vi, pi):
    g = 9.8
    return g / 2 * t**2 + vi + pi


class LivePlot:
    def __init__(self, t, x, y):
        pg.mkQApp()

        proc = proc = mp.QtProcess()
        rpg = proc._import("pyqtgraph")
        self.plot = rpg.plot(name="position")

        self.t = t
        self.x = x
        self.y = y

        self.plot.setLabel(axis="bottom", text="Time (s)")
        self.plot.setLabel(axis="left", text="Position (m)")
        self.plot.setWindowTitle("Projectile Time vs Position")
        self.legend = self.plot.addLegend()
        self.xplot = self.plot.plot([], [], pen=None, symbolPen="b", name="x")
        self.xprediction = self.plot.plot([], [], pen="c", name="x prediction")
        self.yplot = self.plot.plot([], [], pen=None, symbolPen="r", name="y")
        self.yprediction = self.plot.plot([], [], pen="m", name="y prediction")
        self.yprediction_no_g = self.plot.plot(
            [], [], pen="y", name="y prediction without fixed gravity"
        )

    def update(self):
        self.xplot.setData(self.t, self.x, _callSync="off")
        self.yplot.setData(self.t, self.y, _callSync="off")

        # if len(self.t) > 2:
        #     self.graph_lines(self.t, self.x, self.y)

    def graph_lines(self, t, x, y):
        y_coeffs_unfixed = np.polyfit(t, y, 2)
        print(y_coeffs_unfixed)
        y_coeffs = np.polyfit(t, [y[i] - 4.9 * t[i] ** 2 for i in range(len(t))], 1)
        print(y_coeffs)
        x_coeffs = np.polyfit(t, x, 1)
        print(x_coeffs)

        y_func = np.poly1d([4.9] + list(y_coeffs))
        y_func_unfixed = np.poly1d(y_coeffs_unfixed)
        x_func = np.poly1d(x_coeffs)

        times_to_graph = np.linspace(0, 1, 50)

        y_to_graph = y_func(times_to_graph)
        y_to_graph_unfixed = y_func_unfixed(times_to_graph)
        x_to_graph = x_func(times_to_graph)

        self.yprediction.setData(times_to_graph, y_to_graph)
        self.yprediction_no_g.setData(times_to_graph, y_to_graph_unfixed)
        self.xprediction.setData(times_to_graph, x_to_graph)

    def graph_limited_lines(self, points):
        if points < 2:
            print("points must be 2 or higher")
            return
        self.graph_lines(self.t[:points], self.x[:points], self.y[:points])
