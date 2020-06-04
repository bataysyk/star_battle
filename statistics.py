import pandas as pd
import matplotlib.pyplot as plt


class Statistic(object):

    def create_graph(self):

        file = pd.read_csv("records.csv", index_col=0)
        x = file.index
        y = file["killed"]
        plt.bar(x, y, label="line 1")
        plt.xlabel = ("Time (s)")
        plt.ylabel = ("Killed")
        plt.savefig("media/Figyre_1.png")
