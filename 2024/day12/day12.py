import time
from enum import Enum
from typing import Self

import networkx as nx
from matplotlib import pyplot as plt
from shapely import MultiPoint


class Direction(Enum):
    W = (-1, 0)
    N = (0, -1)
    E = (1, 0)
    S = (0, 1)

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]


class Plot:
    def __init__(self, x: int, y: int, plant: str):
        self.x = x
        self.y = y
        self.plant = plant
        # self.sq_points = [[x, -y], [x + 1, -y], [x, -y - 1], [x + 1, -y - 1], [x, -y]]

    def is_adj(self, plot: Self) -> bool:
        return self.plant == plot.plant

    def __repr__(self):
        return self.plant


class Region:
    def __init__(self, plots: list[Plot]):
        self.plant = plots[0].plant
        self.plots: list[Plot] = plots
        self.points: MultiPoint = MultiPoint([[p.x, -p.y] for p in self.plots])
        self.interior_regions: list[Self] = []

        self.polygon = self.points.buffer(0.5, cap_style="square", join_style="mitre")
        self.area = self.polygon.area
        self.perimeter = self.polygon.exterior.length + sum([i.length for i in list(self.polygon.interiors)])

    def __repr__(self):
        return f"Region({self.plant}, area={self.area})"


class Garden:
    def __init__(self, plots: list[list[Plot]]):
        self.plots: list[list[Plot]] = plots
        self.regions: list[Region] = []
        self.g = nx.Graph()

    def get_fence_cost(self) -> int:
        cost = 0
        for region in self.regions:
            region_cost = region.perimeter * region.area
            cost += region_cost

        return cost

    def build_edges(self):
        edges = []
        for row in self.plots:
            for plot in row:
                self.g.add_node(plot)
                for adj_plot in self._get_adj_plots(plot):
                    edges.append((plot, adj_plot))

        self.g.add_edges_from(edges)

    def build_regions(self):
        for plots in nx.connected_components(self.g):
            self.regions.append(Region(list(plots)))

    def _get_adj_plots(self, plot: Plot) -> list[Plot]:
        adj_plots: list[Plot] = []
        for d in Direction:
            adj_x, adj_y = plot.x + d.x, plot.y + d.y
            if min(adj_x, adj_y) < 0 or adj_x >= len(self.plots[0]) or adj_y >= len(self.plots):
                continue

            adj_plot = self.plots[adj_y][adj_x]
            if plot.is_adj(adj_plot):
                adj_plots.append(adj_plot)

        return adj_plots

    def display(self):
        for row in self.plots:
            print("".join([str(plot) for plot in row]))

        nx.draw(self.g, with_labels=True)
        plt.show()


def main():

    plots: list[list[Plot]] = []
    with open("../inputs/day12_input.txt", encoding="utf-8") as f:
        read_data = f.read()
        for y, row in enumerate(read_data.splitlines()):
            plot_row: list[Plot] = []
            for x, plant in enumerate(row):
                plot_row.append(Plot(x, y, plant))

            plots.append(plot_row)

    garden = Garden(plots)
    garden.build_edges()
    garden.build_regions()

    print(garden.get_fence_cost())


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Runtime: {round(time.time() - start, 3)} seconds")