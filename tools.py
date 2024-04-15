import numpy as np
import matplotlib.pyplot as plt


def get_array(filename):
    return np.loadtxt(filename)


def plot_file(filename):
    data = get_array(filename)
    fig, ax = plt.subplots(1,1)
    ax.plot(np.log10(data[:,0]), data[:,1], "r-", label=r"$\alpha=2.35$, $M_{up}=100 M_\odot$")
    ax.plot(np.log10(data[:,0]), data[:,2], "g--", label=r"$\alpha=3.30$, $M_{up}=100 M_\odot$")
    ax.plot(np.log10(data[:,0]), data[:,3], "b:", label=r"$\alpha=2.35$, $M_{up}=30 M_\odot$")

    ax.invert_yaxis()
    ax.set_xlim(6, 9)

    ax.set_xlabel("log (Time [yr])")
    ax.set_ylabel("Value")
    plt.legend(loc="upper right")
    plt.show()
