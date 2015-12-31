import numpy as np
import matplotlib.pyplot as plt
# import matplotlib
from scipy.spatial import Voronoi, voronoi_plot_2d


def random_numbers():
    numbers = []
    for x in range(0, 22):
        for y in range(0, 22):
            ysize = x * 12 + np.random.randint(-6, 6)
            if x % 2 == 0:
                xsize = y * 12 + np.random.randint(-6, 6)
            else:
                xsize = y * 12 + 6 + np.random.randint(-6, 6)
            pair = [xsize, ysize]
            numbers.append(pair)
    return numbers


class VoronoiPlot:
    def __init__(self, seed=0):
        self.index = []
        if seed:
            np.random.seed(seed)
        self.coords = random_numbers()
        self.vor = Voronoi(self.coords)
        voronoi_plot_2d(self.vor)

        # set background lightblue
        ax = plt.gca()
        ax.set_axis_bgcolor('lightblue')

    @staticmethod
    def is_border(polygon):
        for vertex in polygon:
            if vertex[0] < 0 or vertex[0] > 228.624 or vertex[1] < 0 or vertex[1] > 201:
                return True

    def is_sea(self, polygon):
        shared_vertices_sea = 0
        shared_vertices_land = 0
        for tile in self.index:
            for i in tile[0]:
                for j in polygon:
                    if i[0] == j[0] and i[1] == j[1]:
                        if tile[1] == 'sea' or tile[1] == 'border':
                            shared_vertices_sea += np.amax(i) - np.amin(i)
                            print(u"max: {0:f} | min: {1:f}".format(np.amax(i), np.amin(i)))
                    #    elif shared_vertices_land < 2:
                    #        shared_vertices_land += 1
                        elif np.random.randint(0, 2) == 1:
                            shared_vertices_land += np.amax(i) - np.amin(i)
        print(u"shared with: land {0:f} | sea: {1:f}".format(shared_vertices_land, shared_vertices_sea))
        if shared_vertices_sea > shared_vertices_land:
            return True
        return False

    def generate(self):
        # colorize
        for region in self.vor.regions:
            if region and -1 not in region:
                polygon = [self.vor.vertices[i] for i in region]

                if self.is_border(polygon):
                    self.index.append([polygon, 'border'])
                elif self.is_sea(polygon):
                    self.index.append([polygon, 'sea'])
                else:
                    self.index.append([polygon, 'land'])

    def regenerate(self):
        for tile in self.index:
            if self.is_border(tile[0]):
                tile[1] = 'border'
            elif self.is_sea(tile[0]):
                tile[1] = 'sea'
            else:
                tile[1] = 'land'

    def color(self):
        for tile in self.index:
            if tile[1] == 'border':
                plt.fill(*zip(*tile[0]), color='blue')
            elif tile[1] == 'sea':
                plt.fill(*zip(*tile[0]), color='lightblue')
            elif tile[1] == 'land':
                plt.fill(*zip(*tile[0]), color='yellow')


if __name__ == '__main__':
    plot = VoronoiPlot()
    plot.generate()
    plot.regenerate()
    plot.color()
    plt.axis([0, 228.624, 0, 201])

    plot2 = VoronoiPlot()
    plot2.generate()
    plot2.regenerate()
    plot2.color()
    plt.axis([0, 228.624, 0, 201])

    plot3 = VoronoiPlot()
    plot3.generate()
    plot3.regenerate()
    plot3.color()
    plt.axis([0, 228.624, 0, 201])

    plot4 = VoronoiPlot()
    plot4.generate()
    plot4.regenerate()
    plot4.color()
    plt.axis([0, 228.624, 0, 201])

    plt.show()
