from PyQt6.QtCore import QTimer
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
import os

import hashlib

import numpy as np
import pandas as pd

Q_COLORS = ["r", "g", "b", "c", "m", "y"]


class LivePlot:
    def __init__(self, points_filename, lines_filename):
        self.app = pg.mkQApp()

        self.plot = pg.plot(name="position")

        self.points_file = points_filename
        self.lines_file = lines_filename

        self.plot.setLabel(axis="bottom", text="Time (s)")
        self.plot.setLabel(axis="left", text="Position (m)")
        self.plot.setWindowTitle("Projectile Time vs Position")
        self.plot.addLegend()

        self.xplot = self.plot.plot([], [], pen=None, symbolPen="b", name="x")
        self.yplot = self.plot.plot([], [], pen=None, symbolPen="r", name="y")

        self.lines = {}

    def plot_points(self):
        points_df = pd.read_csv(self.points_file, header=None)
        hash = hashlib.sha1(pd.util.hash_pandas_object(points_df).values).hexdigest()
        if hasattr(self, "points_hash") and self.points_hash == hash:
            return

        self.points_hash = hash

        t = points_df.iloc[0]
        x = points_df.iloc[1]
        y = points_df.iloc[2]

        self.max_t = max(t[len(t) - 1], 1)

        self.xplot.setData(t, x)
        self.yplot.setData(t, y)

    def update(self):
        self.plot_points()
        self.graph_lines()

        return

    def graph_lines(self):
        lines_df = pd.read_csv(self.lines_file)

        hash = hashlib.sha1(pd.util.hash_pandas_object(lines_df).values).hexdigest()
        if hasattr(self, "lines_hash") and self.lines_hash == hash:
            return

        self.lines_hash = hash

        times_to_graph = np.linspace(0, self.max_t, 50)

        for line_name in list(self.lines):
            if line_name not in lines_df.columns:
                self.plot.removeItem(self.lines[line_name])
                del self.lines[line_name]

        for line_name, line_coeffs in lines_df.items():
            func = np.poly1d(list(line_coeffs))
            y_to_graph = func(times_to_graph)

            if not line_name in self.lines:
                self.lines[line_name] = self.plot.plot(
                    times_to_graph, y_to_graph, name=line_name
                )
            else:
                self.lines[line_name].setData(times_to_graph, y_to_graph)

        line_names = list(self.lines)
        for i in range(len(line_names)):
            self.lines[line_names[i]].setPen(Q_COLORS[i % len(Q_COLORS)])


import write_data

live_plot = LivePlot(write_data.POINTS_FILENAME, write_data.COEFFS_FILENAME)

timer = QTimer()
timer.setInterval(30)
timer.timeout.connect(live_plot.update)
timer.start()

sys.exit(live_plot.app.exec())
