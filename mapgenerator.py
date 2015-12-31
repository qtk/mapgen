import matplotlib.pyplot as plt
import numpy as np

# import matplotlib
from scipy.spatial import Voronoi, voronoi_plot_2d


def random_numbers():  # generates the input points for the voronoi diagram
    numbers = []
    for x in range(0, 22):  # first, it fills the area with points in a grid.
        for y in range(0, 22):
            ysize = x * 12 + np.random.randint(-6, 6)
            if x % 2 == 0:  # every even row is moved to create hexagon-like points
                xsize = y * 12 + np.random.randint(-6, 6)  # points are slightly moved around to create quasi-randomness
            else:
                xsize = y * 12 + 6 + np.random.randint(-6, 6)
            pair = [xsize, ysize]
            numbers.append(pair)
    return numbers


class VoronoiPlot:
    def __init__(self, seed=0):
        if seed:
            np.random.seed(seed)
        self.beach = 0
        self.index = []
        self.coords = random_numbers()
        self.vor = Voronoi(self.coords)
        voronoi_plot_2d(self.vor)

        # set background to lightblue, to make te border sea.
        ax = plt.gca()
        ax.set_axis_bgcolor('blue')

    def adjacent_tiles(self, polygon, regen=0):
        shared_points_sea = 0
        shared_points_land = 0
        shared_points_beach = 0
        for tile in self.index:
            for i in tile[0]:
                for j in polygon:
                    if i[0] == j[0] and i[1] == j[1]:  # coordinates are the same
                        if tile[1] == 'sea' or tile[1] == 'border':
                            shared_points_sea += 1
                        elif tile[1] == 'land':
                            shared_points_land += 1
                        elif tile[1] == 'beach':
                            shared_points_beach += 1
        print(u"shared with: land {0:d} | sea: {1:d} | beach: {2:d}".format(shared_points_land, shared_points_sea,
                                                                            shared_points_beach))
        if shared_points_sea == 0 and (shared_points_land or shared_points_beach):
            if np.random.randint(0, 50) == 1:
                print('lake')
                return 'lake'
            else:
                print('land')
                return 'land'
        elif shared_points_sea:
            if not regen and self.beach < 3:
                if (shared_points_beach or shared_points_land) or np.random.randint(0, 160) == 1:
                    self.beach += 1
                    print('beach')
                    return 'beach'
                else:
                    print('sea')
                    return 'sea'
            else:
                if shared_points_beach or shared_points_land:
                    print('beach')
                    return 'beach'
                else:
                    print('sea')
                    return 'sea'
        else:
            print('sea')
            return 'sea'

    @staticmethod
    def is_border(polygon):
        for vertex in polygon:
            if vertex[0] < 0 or vertex[0] > 228.624 or vertex[1] < 0 or vertex[1] > 201:
                return True

    def generate(self):
        # adds each tile to index and gives it a surface-type
        for region in self.vor.regions:
            if region and -1 not in region:
                polygon = [self.vor.vertices[i] for i in region]
                if not self.is_border(polygon):
                    area_type = self.adjacent_tiles(polygon)
                    self.index.append([polygon, area_type])
                else:
                    self.index.append([polygon, 'border'])
        self.__regenerate()
        self.__regenerate()
        self.__regenerate()
        self.__color()

    def __regenerate(self):
        # rechecks every surface type
        for tile in self.index:
            if not self.is_border(tile[0]):
                area_type = self.adjacent_tiles(tile[0], regen=1)
                tile[1] = area_type

    def __color(self):
        # colors each tile according to the surface type
        plt.figure(2)
        plt.axis([0, 228.624, 0, 201])
        for tile in self.index:
            if tile[1] == 'border' or tile[1] == 'sea':
                plt.fill(*zip(*tile[0]), color='blue')
            if tile[1] == 'lake':
                plt.fill(*zip(*tile[0]), color='lightblue')
            elif tile[1] == 'beach':
                plt.fill(*zip(*tile[0]), color='yellow')
            elif tile[1] == 'land':
                plt.fill(*zip(*tile[0]), color='green')
        plt.savefig('without-lines.png')

        plt.figure(1)
        plt.axis([0, 228.624, 0, 201])
        for tile in self.index:
            if tile[1] == 'border' or tile[1] == 'sea':
                plt.fill(*zip(*tile[0]), color='blue')
            if tile[1] == 'lake':
                plt.fill(*zip(*tile[0]), color='lightblue')
            elif tile[1] == 'beach':
                plt.fill(*zip(*tile[0]), color='yellow')
            elif tile[1] == 'land':
                plt.fill(*zip(*tile[0]), color='green')
        plt.savefig('with-lines.png')


if __name__ == '__main__':
    plot = VoronoiPlot()
    plot.generate()
    plt.axis([0, 228.624, 0, 201])  # size is weird because it will be filled up by hexagons
    print(plot.beach)
    plt.show()
