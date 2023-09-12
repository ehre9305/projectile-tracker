import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def time_to_y_pos(t, vi, pi):
    g = 9.8
    return g / 2 * t**2 + vi + pi


class LivePlot:
    def __init__(self, points_filename, lines_filename):
        fig, self.ax = plt.subplots()

        self.points_file = points_filename
        self.lines_file = lines_filename

        plt.xlabel("Time (s)")
        plt.ylabel("Position (m)")
        plt.title("Projectile Time vs Position")
        self.ani = animation.FuncAnimation(
            fig, self.update, interval=50, blit=False, save_count=10
        )

    def plot_points(self):
        points_df = pd.read_csv(self.points_file, header=None)
        t = points_df.iloc[0]
        x = points_df.iloc[1]
        y = points_df.iloc[2]

        self.max_t = max(t[len(t) - 1], 1)

        self.ax.clear()
        (self.xplot,) = self.ax.plot(t, x, "bo", label="x")
        (self.yplot,) = self.ax.plot(t, y, "ro", label="y")

    def update(self, _):
        self.plot_points()
        self.graph_lines()

        plt.legend()
        return (self.xplot, self.yplot, self.ax)

    def graph_lines(self):
        times_to_graph = np.linspace(0, self.max_t, 50)

        lines_df = pd.read_csv(self.lines_file)

        for line_name, line_coeffs in lines_df.items():
            func = np.poly1d(list(line_coeffs))
            y_to_graph = func(times_to_graph)

            self.ax.plot(times_to_graph, y_to_graph, label=line_name)

    def graph_limited_lines(self, points):
        if points < 2:
            print("points must be 2 or higher")
            return
        self.graph_lines(self.t[:points], self.x[:points], self.y[:points])


import write_data

live_plot = LivePlot(write_data.POINTS_FILENAME, write_data.COEFFS_FILENAME)
plt.show()
