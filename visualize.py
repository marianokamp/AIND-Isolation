import matplotlib.pyplot as plt
import numpy as np

def visualize_as_bar(d, title=None):

    positions = np.arange(len(d))*1.1

    no_of_dimensions = len(next(iter(d.values())))

    my_colors = 'rgbkymc'
    for dim in range(0, no_of_dimensions):
        data = []
        for label in d.keys():
            data += [d[label][dim]]
        plt.bar(positions+dim*0.25, data, width=0.25, color=my_colors[dim])

    plt.xticks(positions+0.25, d.keys())
    if title:
        plt.title(title)

    plt.savefig("results_graph.png")

if __name__ == "__main__":

    d = {}
    d['mixed\ncentrality'] = [4, 11, 12]
    d['something \n else'] =[-8, +5, 7]
    d['something \n else2'] =[-5, 5, 7]

    visualize_as_bar(d, "some title")
