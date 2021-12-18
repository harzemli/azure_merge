import calculator as calculate
import coordinates
import matplotlib.pyplot as plt
import numpy as np


def plot(track):
    """ draw track"""
    colors = np.arange(len(track))
    x, y = coordinates.extract_x_and_y_values_lists(track)
    plt.scatter(x, y, c=colors)
    for i, number in enumerate(colors):
        known_radius = calculate.radius(x[i], y[i], x[i-1], y[i-1], x[i-2], y[i-2])
        fulltext = "Number: {}\nRadius: {}".format(number, round(known_radius))
        plt.annotate(fulltext, (x[i], y[i]), fontsize=7)
        plt.gca().invert_yaxis()
    plt.show()
