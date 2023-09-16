from PyQt6.QtCore import QTimer
import pyqtgraph as pg
import sys
import os

import numpy as np
import pandas as pd

Q_COLORS = ["r", "g", "b", "c", "m", "y"]


class LivePlot:
    def __init__(self, points_filename, lines_filename):
        self.app = pg.mkQApp()

        self.layout = pg.GraphicsLayoutWidget()
        self.layout.setWindowTitle("Projectile graphs")
        self.layout.show()

        self.time_plot = self.layout.addPlot(name="position v time")
        self.layout.nextRow()
        self.pos_plot = self.layout.addPlot(name="position v position")
        self.pos_lines = []

        self.points_file = points_filename
        self.lines_file = lines_filename

        self.pos_plot.setLabel(axis="bottom", text="Position x (m)")
        self.pos_plot.setLabel(axis="left", text="Position y (m)")
        self.pos_plot.addLegend()

        self.time_plot.setLabel(axis="bottom", text="Time (s)")
        self.time_plot.setLabel(axis="left", text="Position (m)")
        self.time_plot.addLegend()

        self.xVyPlot = self.pos_plot.plot(
            [], [], pen=None, symbolPen="b", name="x vs y"
        )

        self.xplot = self.time_plot.plot([], [], pen=None, symbolPen="b", name="x")
        self.yplot = self.time_plot.plot([], [], pen=None, symbolPen="r", name="y")

        self.lines = {}

    def plot_points(self):
        mod_time = os.path.getmtime(self.points_file)
        if hasattr(self, "points_time") and self.points_time == mod_time:
            return
        self.points_time = mod_time

        points_df = pd.read_csv(self.points_file, header=None)

        self.points_hash = hash

        t = points_df.iloc[0]
        x = points_df.iloc[1]
        y = points_df.iloc[2]

        self.max_t = max(t[len(t) - 1], 1)

        self.xplot.setData(t, x)
        self.yplot.setData(t, y)

        self.xVyPlot.setData(x, y)

    def update(self):
        self.plot_points()
        self.graph_lines()

        return

    def graph_lines(self):
        mod_time = os.path.getmtime(self.lines_file)
        if hasattr(self, "lines_time") and self.lines_time == mod_time:
            return
        self.lines_time = mod_time

        lines_df = pd.read_csv(self.lines_file)

        times_to_graph = np.linspace(0, self.max_t, 50)

        for line_name in list(self.lines):
            if line_name not in lines_df.columns:
                self.time_plot.removeItem(self.lines[line_name])
                del self.lines[line_name]

        for line_name, line_coeffs in lines_df.items():
            func = np.poly1d(list(line_coeffs))
            y_to_graph = func(times_to_graph)

            if not line_name in self.lines:
                self.lines[line_name] = self.time_plot.plot(
                    times_to_graph, y_to_graph, name=line_name
                )
            else:
                self.lines[line_name].setData(times_to_graph, y_to_graph)

        line_names = list(self.lines)
        for i in range(len(line_names)):
            self.lines[line_names[i]].setPen(Q_COLORS[i % len(Q_COLORS)])

        x_data = None
        for line in self.pos_lines:
            self.pos_plot.removeItem(line)
        self.pos_lines = []
        for line in self.lines:
            if x_data is None:
                x_data = self.lines[line].getData()[1]
            else:
                cur_line = self.lines[line]
                self.pos_lines.append(
                    self.pos_plot.plot(
                        x_data,
                        cur_line.getData()[1],
                        name=cur_line.name(),
                        pen=cur_line.opts["pen"],
                    ),
                )


import write_data

live_plot = LivePlot(write_data.POINTS_FILENAME, write_data.COEFFS_FILENAME)

timer = QTimer()
timer.setInterval(30)
timer.timeout.connect(live_plot.update)
timer.start()

sys.exit(live_plot.app.exec())
