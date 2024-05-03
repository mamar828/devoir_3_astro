import numpy as np
import scipy
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker

from tools import get_array, plot_file


def make_time_evolution_figure(star_formation_law: str):
    law = star_formation_law
    law_f = law[:4]         # used in the filenames

    fig, axs = plt.subplots(3, 2, sharex=True, figsize=(6.4,8))

    def plot_file(axis, filename, color):
        for file_column, style in enumerate(["solid", "dashed"]):
            array = get_array(filename)
            axs[axis].plot(np.log10(array[:,0]), array[:,file_column+1], linestyle=style, color=color, linewidth=1)
        axs[axis].set_xlim(6, 9)
        axs[axis].xaxis.set_major_locator(ticker.MultipleLocator(0.5))
        axs[axis].xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
        axs[axis].xaxis.set_tick_params(direction="in", which="both")
        axs[axis].tick_params(direction="in")

    plot_file((0, 0), f"data/colors/b_v/{law}/bv_{law_f}_a.dat", "cornflowerblue")
    plot_file((0, 0), f"data/colors/b_v/{law}/bv_{law_f}_e.dat", "crimson")
    axs[0, 0].set_ylim(-0.25, 0.3)
    axs[0, 0].invert_yaxis()
    axs[0, 0].set_title("(B-V)")

    plot_file((0, 1), f"data/colors/u_b/{law}/ub_{law_f}_a.dat", "cornflowerblue")
    plot_file((0, 1), f"data/colors/u_b/{law}/ub_{law_f}_e.dat", "crimson")
    axs[0, 1].set_ylim(-1.5, 0)
    axs[0, 1].invert_yaxis()
    axs[0, 1].set_title("(U-B)")

    plot_file((1, 0), f"data/halpha_width/{law}/wha_{law_f}_a.dat", "cornflowerblue")
    plot_file((1, 0), f"data/halpha_width/{law}/wha_{law_f}_e.dat", "crimson")
    axs[1, 0].set_ylim(-1, 4)
    axs[1, 0].set_title(r"Largeur équivalente de H$\alpha$")

    plot_file((2, 0), f"data/photon_number/below_228/{law}/228_{law_f}_a.dat", "cornflowerblue")
    plot_file((2, 0), f"data/photon_number/below_228/{law}/228_{law_f}_e.dat", "crimson")
    axs[2, 0].set_ylim(44, 52)
    axs[2, 0].set_title(r"Nombre de photons sous 228 $\rm\AA$")

    plot_file((2, 1), f"data/photon_number/below_912/{law}/912_{law_f}_a.dat", "cornflowerblue")
    plot_file((2, 1), f"data/photon_number/below_912/{law}/912_{law_f}_e.dat", "crimson")
    axs[2, 1].set_ylim(44, 54)
    axs[2, 1].set_title(r"Nombre de photons sous 912 $\rm\AA$")

    axs[0, 0].set_ylabel("Indice de couleur [-]")
    axs[1, 0].set_ylabel(r"log (W(H$\alpha$) [$\rm\AA$])")
    axs[2, 0].set_ylabel(r"log (N(H$^\degree$) [photons s$^{-1}$])")
    fig.supxlabel("log (Temps [a])")

    axs[1, 1].axis("off")

    fig.legend(handles=[
        mpatches.Patch(color="cornflowerblue", label=r"$Z=0.040$"),
        mpatches.Patch(color="crimson", label=r"$Z=0.001$"),
        mlines.Line2D([], [], color="black", linestyle="solid",  label=r"$\alpha=2.35$, $M_{up}=100\rm\ M_{\odot}$"),
        mlines.Line2D([], [], color="black", linestyle="dashed", label=r"$\alpha=3.30$, $M_{up}=100\rm\ M_{\odot}$")
    ], loc=(0.5755,0.46), prop={'size': 12}
    )

    plt.tight_layout()
    plt.savefig(f"figures/{star_formation_law}_time_evolution.png", dpi=600, bbox_inches="tight")
    # plt.show()


# make_time_evolution_figure("continuous")
# make_time_evolution_figure("instantaneous")


def make_min_max_color_figure():
    fig, axs = plt.subplots(1, 2, figsize=(6.4,3), sharey=True)
    labels = [r"$4$", r"$2$", r"$0.8$", r"$0.4$", r"$0.1$"]
    x = np.arange(len(labels))
    width = 0.2

    def set_axis_params(axis):
        axis.xaxis.set_tick_params(direction="in", which="both")
        axis.tick_params(direction="in")

    for ax, i_color, make_legend in zip(axs, ["b_v", "u_b"], [True, False]):
        multiplier = -0.5
        peaks = []
        for letter in ["a", "b", "c", "d", "e"]:
            for law in ["continuous", "instantaneous"]:
                array = get_array(f"data/colors/{i_color}/{law}/{i_color[0]+i_color[2]}_{law[:4]}_{letter}.dat")
                time_upper_limit = 10**7.5
                i = np.argmin(np.abs(array[:,0] - time_upper_limit))
                for row in [1, 2]:
                    peaks.append([np.max(array[:i,row]) - np.min(array[:i,row])])

        peaks_array = np.array(peaks).reshape(5, 4)
        plot_data = [
            [r"Continue, $\alpha=2.35$", peaks_array[:,0], "orange", ""],
            [r"Continue, $\alpha=3.30$", peaks_array[:,1], "orange", "//"],
            [r"Instantanée, $\alpha=2.35$", peaks_array[:,2], "green", ""],
            [r"Instantanée, $\alpha=3.30$", peaks_array[:,3], "green", "//"]
        ]

        for name, data, color, hatch in plot_data:
            offset = width * multiplier
            rects = ax.bar(x + offset, data, width, color=color, label=name, hatch=hatch)
            # ax.bar_label(rects, fmt="%.2f")
            multiplier += 1

        ax.set_ylabel(
            f"Différence entre les extremums\nd'indice de couleur"+ rf" $({i_color[0].upper()}-{i_color[-1].upper()})$")
        ax.set_xticks(x + width, labels)
        ax.set_ylim(0, 1)
        set_axis_params(ax)

        if make_legend:
            fig.legend(loc=(0.2,0.02), ncols=2)#, bbox_to_anchor=(0.5, 0.1))
            
    fig.supxlabel(r"Métallicité [$10^{-2}$]")
    fig.subplots_adjust(bottom=0.13)
    fig.text(0.5,-0.14, "this text stretches the figure !", color="white")
    plt.savefig("figures/min_max_color.png", dpi=600, bbox_inches="tight")
    # plt.show()


# make_min_max_color_figure()


def make_slope_halpha_figure():
    fig, ax = plt.subplots(1, 1, figsize=(6.4,3.5), sharey=True)
    labels = [r"$4$", r"$2$", r"$0.8$", r"$0.4$", r"$0.1$"]
    x = np.arange(len(labels))
    width = 0.35

    def set_axis_params(axis):
        axis.xaxis.set_tick_params(direction="in", which="both")
        axis.tick_params(direction="in")

    multiplier = 0.5
    slopes = []
    for letter in ["a", "b", "c", "d", "e"]:
        law = "continuous"
        array = get_array(f"data/halpha_width/{law}/wha_{law[:4]}_{letter}.dat")
        time_upper_limit = 10**7
        i = np.argmin(np.abs(array[:,0] - time_upper_limit))
        for row in [1, 2]:
            # fit = scipy.stats.linregress(np.log10(array[i:,0]), array[i:,row])
            # print(fit.slope)
            # plt.plot(np.log10(array[:,0]), array[:,row])
            # plt.xlim(6, 9)
            # plt.show()
            slopes.append(-scipy.stats.linregress(np.log10(array[i:,0]), array[i:,row]).slope)

    peaks_array = np.array(slopes).reshape(5, 2)
    plot_data = [
        [r"$\alpha=2.35$", peaks_array[:,0], ""],
        [r"$\alpha=3.30$", peaks_array[:,1], "//"]
    ]

    for name, data, hatch in plot_data:
        offset = width * multiplier
        rects = ax.bar(x + offset, data, width, color="orange", label=name, hatch=hatch)
        ax.bar_label(rects, fmt="%.2f")
        multiplier += 1

    ax.set_ylabel("Pente de la largeur équivalente\n"+r"H$\alpha$ décroissante en valeur absolue")
    ax.set_xticks(x + width, labels)
    ax.set_ylim(0, 1)
    set_axis_params(ax)

    ax.legend(loc="upper left", ncols=1)
            
    ax.set_xlabel(r"Métallicité [$10^{-2}$]")
    # fig.subplots_adjust(bottom=0.13)
    # fig.text(0.5,-0.14, "this text stretches the figure !", color="white")
    plt.savefig("figures/slope_halpha.png", dpi=600, bbox_inches="tight")
    # plt.show()


# make_slope_halpha_figure()


def make_slope_halpha_instantaneous_figure():
    fig, axs = plt.subplots(1, 2, figsize=(8,4), sharey=True)
    labels = [r"$0.04$", r"$0.02$", r"$0.008$", r"$0.004$", r"$0.001$"]
    x = np.arange(len(labels))
    width = 0.2

    def set_axis_params(axis):
        axis.set_xlim(6, 9)
        axis.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
        axis.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
        axis.xaxis.set_tick_params(direction="in", which="both")
        axis.tick_params(direction="in")

    law = "instantaneous"
    array_low = get_array(f"data/halpha_width/{law}/wha_{law[:4]}_a.dat")
    array_high = get_array(f"data/halpha_width/{law}/wha_{law[:4]}_e.dat")
    axs[0].fill_between(np.log10(array_low[:,0]), array_low[:,1], array_high[:,1], color="green", hatch="\\\\", alpha=0.5,
                    label=r"$\alpha=2.35$", edgecolor='black')
    axs[0].fill_between(np.log10(array_low[:,0]), array_low[:,2], array_high[:,2], color="green", hatch="//", alpha=0.5,
                    label=r"$\alpha=3.30$", edgecolor='black')
    # axs[0].plot(np.log10(array_low[:,0]), array_low[:,2], color="black", label=r"$Z=0.04$")
    # axs[0].plot(np.log10(array_low[:,0]), array_high[:,1], color="grey", label=r"$Z=0.001$")
    for letter, label in zip(["a", "b", "c", "d", "e"], labels):
        array = get_array(f"data/halpha_width/{law}/wha_{law[:4]}_{letter}.dat")
        axs[1].plot(np.log10(array[:,0]), array[:,1], label=(r"$Z=$"+label))

    fig.supylabel(r"log (W(H$\alpha$) [$\rm\AA$])")
    set_axis_params(axs[0])
    set_axis_params(axs[1])

    axs[0].legend(loc="lower left", ncols=1)
    axs[1].legend(loc="lower left", ncols=1)
    fig.subplots_adjust(bottom=0.125)
    fig.supxlabel("log (Temps [a])")
    plt.savefig("figures/slope_halpha_instantaneous_both.png", dpi=600, bbox_inches="tight")
    # plt.show()


# make_slope_halpha_instantaneous_figure()


def make_photons_figure():
    fig, axs = plt.subplots(1, 2, figsize=(6.4,3), sharey=True)
    labels = [r"$4$", r"$2$", r"$0.8$", r"$0.4$", r"$0.1$"]
    x = np.arange(len(labels))
    width = 0.2

    def set_axis_params(axis):
        axis.xaxis.set_tick_params(direction="in", which="both")
        axis.tick_params(direction="in")

    for ax, no, make_legend in zip(axs, ["228", "912"], [True, False]):
        multiplier = -0.5
        vals = []
        for letter in ["a", "b", "c", "d", "e"]:
            for law in ["continuous", "instantaneous"]:
                array = get_array(
                    f"data/photon_number/below_{no}/{law}/{no}_{law[:4]}_{letter}.dat")
                for row in [1, 2]:
                    vals.append(max(array[-1,row], 0))
                    # if law == "instantaneous": 
                    #     plt.plot(np.log10(array[:,0]), array[:,row])
                    #     plt.xlim(6, 9)
                    #     plt.show()

        val_array = np.array(vals).reshape(5, 4)
        plot_data = [
            [r"Continue, $\alpha=2.35$", val_array[:,0], "orange", ""],
            [r"Continue, $\alpha=3.30$", val_array[:,1], "orange", "//"],
            [r"Instantanée, $\alpha=2.35$", val_array[:,2], "green", ""],
            [r"Instantanée, $\alpha=3.30$", val_array[:,3], "green", "//"]
        ]

        for name, data, color, hatch in plot_data:
            offset = width * multiplier
            rects = ax.bar(x + offset, data, width, color=color, label=name, hatch=hatch)
            # ax.bar_label(rects, fmt="%.2f")
            multiplier += 1

        ax.set_ylabel("Nombre de photons par\n" + f"seconde sous {no}" + r"$\AA$ après 1 Ga")
        ax.set_xticks(x + width, labels)
        ax.set_ylim(0, 55)
        set_axis_params(ax)

        if make_legend:
            fig.legend(loc=(0.2,0.02), ncols=2)#, bbox_to_anchor=(0.5, 0.1))
            
    fig.supxlabel(r"Métallicité [$10^{-2}$]")
    fig.subplots_adjust(bottom=0.13)
    fig.text(0.5,-0.14, "this text stretches the figure !", color="white")
    plt.savefig("figures/photons.png", dpi=600, bbox_inches="tight")
    # plt.show()


# make_photons_figure()
