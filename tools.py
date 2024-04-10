import numpy as np
import matplotlib.pyplot as plt


def get_array(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        
    data = []
    for line in lines:
        splitted_line = line.split(" ")
        data.append([float(value) for value in splitted_line if not value in ["", "\n"]])
        
    return np.array(data)


def plot_file(filename):
    data = get_array(filename)
    fig, ax = plt.subplots(1,1)
    ax.plot(data[:,0], data[:,1], "r-")
    ax.plot(data[:,0], data[:,2], "g--")
    ax.plot(data[:,0], data[:,3], "b:")

    ax.invert_yaxis()
    ax.set_xscale("log")
    ax.set_xlim(10**6, 10**9)

    ax.set_xlabel("Time [yr]")
    ax.set_ylabel("Value")
    plt.show()
