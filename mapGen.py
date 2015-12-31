import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from operator import itemgetter
import random
np.random.seed(1337)

def zip_coords(points):
    coords = list(zip(points[0], points[1]))
    coords.sort(key=itemgetter(1))
    coords.sort(key=itemgetter(0))
    return coords


def generate_random_points(n):
    points = np.random.randint(100, size=(2, n))
    coords = zip_coords(points)
    return points, coords


points, coords = generate_random_points(100)

print(coords)
plt.scatter(points[0], points[1])
plt.axis([0, 100, 0, 100])
# vor = Voronoi(coords)
# voronoi_plot_2d(vor)
