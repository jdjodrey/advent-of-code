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

    def get_num_sides(self) -> int:
        if self.area == 1 or self.area == 2:
            return 4

        b = self.polygon.exterior

        side = [b.coords[0]]
        current_direction = None
        num_sides = 0
        coords = list(b.coords) + [b.coords[0]]
        for idx, p1 in enumerate(coords):
            if idx + 1 < len(coords):
                p2 = coords[idx + 1]
                for d in Direction:
                    if d.x + p1[0] == p2[0] and p1[1] - d.y == p2[1]:
                        if current_direction is None:
                            current_direction = d
                            side.append(p2)
                        elif current_direction == d:
                            side.append(p2)
                        else:
                            current_direction = d
                            num_sides += 1
                            side = []

                        break

        # Sometimes have an off-by-one error, so if the num sides is odd, add one
        if num_sides % 2 == 1:
            num_sides += 1

        num_sides += sum([r.get_num_sides() for r in self.interior_regions])
        return num_sides

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
            num_sides = region.get_num_sides()
            region_cost = num_sides * region.area
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

        sorted_regions = sorted(self.regions, key=lambda r: r.area)

        while len(sorted_regions):
            r = sorted_regions.pop(0)
            for other_region in sorted_regions:
                if other_region.polygon.boundary.contains(r.polygon.boundary):
                    other_region.interior_regions.append(r)

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