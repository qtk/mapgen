import matplotlib.pyplot as plt
import numpy as np

# import matplotlib
from scipy.spatial import Voronoi, voronoi_plot_2d


def random_numbers():  # generates the input points for the voronoi diagram
    numbers = []
    for x in range(0, 22):  # first, it fills the area with points in a grid.
        for y in range(0, 22):
            ysize = x * 11  # + np.random.randint(-6, 6)
            if x % 2 == 0:  # every even row is moved to create hexagon-like points
                xsize = y * 11  # + np.random.randint(-6, 6)  # points are slightly moved around to create quasi-randomness
            else:
                xsize = y * 11 + 5.5  # + np.random.randint(-6, 6)
            pair = [xsize, ysize]
            numbers.append(pair)
    return numbers


def not_in_shared_points(shared_points, coord):
    for item in shared_points:
        if item[0] == coord[0] and item[1] == coord[1]:
            return False
    return True


class VoronoiPlot:
    def __init__(self, seed=0):
        if seed:
            np.random.seed(seed)
        self.beach = 0
        self.index = []
        self.coords = random_numbers()
        self.vor = Voronoi(self.coords)
        voronoi_plot_2d(self.vor)

    def adjacent_tiles(self, polygon, regen=0):
        shared_points = []
        shared_points_sea = 0
        shared_points_land = 0
        shared_points_beach = 0
        for tile in self.index:
            for i in tile[0]:
                for j in polygon:
                    if i[0] == j[0] and i[1] == j[1] and not_in_shared_points(shared_points,
                                                                              i):  # coordinates are the same
                        shared_points.append(i)
                        if tile[1] == 'sea' or tile[1] == 'border':
                            shared_points_sea += 1
                        elif tile[1] == 'land':
                            shared_points_land += 1
                        elif tile[1] == 'beach':
                            shared_points_beach += 1
        print(
                u"shared with: land {0:d} | sea: {1:d} | beach: {2:d}".format(
                        shared_points_land,
                        shared_points_sea,
                        shared_points_beach))

        if shared_points_sea == 6 or (shared_points_beach == 0 and shared_points_land == 0):
            if not regen and np.random.randint(0, 2):
                print('is beach')
                return 'beach'
            else:
                print('is sea')
                return 'sea'
        if (shared_points_land == 6 or shared_points_beach == 6) and shared_points_sea == 0:
            print('is land')
            return 'land'
        if shared_points_beach >= 1:
            print('is beach')
            return 'beach'


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
        self.__color()

    def __regenerate(self):
        # rechecks every surface type
        for tile in self.index:
            if not self.is_border(tile[0]):
                area_type = self.adjacent_tiles(tile[0], regen=1)
                tile[1] = area_type

    def __color(self):
        # colors each tile according to the surface type
        # plt.figure(2)
        # plt.axis([0, 228.624, 0, 201])
        # for tile in self.index:
        #    if tile[1] == 'border' or tile[1] == 'sea':
        #        plt.fill(*zip(*tile[0]), color='blue')
        #    if tile[1] == 'lake':
        #        plt.fill(*zip(*tile[0]), color='lightblue')
        #    elif tile[1] == 'beach':
        #        plt.fill(*zip(*tile[0]), color='yellow')
        #    elif tile[1] == 'land':
        #        plt.fill(*zip(*tile[0]), color='green')
        # plt.savefig('without-lines.png')

        # set background to lightblue, to make te border sea.
        # ax = plt.gca()
        # ax.set_axis_bgcolor('blue')

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

        # set background to lightblue, to make te border sea.
        ax = plt.gca()
        ax.set_axis_bgcolor('blue')


if __name__ == '__main__':
    plot = VoronoiPlot(1337)
    plot.generate()
    plt.axis([0, 228.624, 0, 201])  # size is weird because it will be filled up by hexagons
    print(plot.beach)
    plt.show()
