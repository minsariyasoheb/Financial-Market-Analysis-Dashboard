import matplotlib.pyplot as plt
import seaborn as sns

class visualizations:
    def __init__(self):
        pass
    
    def line_chart(self, data, title, x_axis, y_axis):
        data.plot(figsize=(10, 5))
        plt.title(title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.legend()
        plt.show()
    
    def hist_chart(self, data, title, x_axis, y_axis, bins=10):
        data.hist(figsize=(10, 5), bins=bins)
        plt.title(title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.legend()
        plt.show()

    def scatter_chart(self, x_data, y_data, title, x_axis, y_axis):
        plt.figure(figsize=(10, 5))
        plt.scatter(x_data, y_data)
        plt.title(title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.show()

    def bar_chart(self, x_data, y_data, title, x_axis, y_axis, horizontal=False):
        plt.figure(figsize=(10, 5))
        if horizontal:
            plt.barh(x_data, y_data)
        else:
            plt.bar(x_data, y_data)
        plt.title(title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.show()

    def heatmap(self, data, title, annot=True, cmap="coolwarm"):
        plt.figure(figsize=(10, 8))
        sns.heatmap(data, annot=annot, cmap=cmap)
        plt.title(title)
        plt.show()