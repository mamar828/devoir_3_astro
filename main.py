import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

from tools import get_array, plot_file


def make_5_panel_figure(star_formation_law: str):
    law = star_formation_law
    law_f = law[:4]         # used in the filenames

    fig, axs = plt.subplots(3, 2, sharex=True, figsize=(6.4,8))

    def plot_file(axis, filename, color):
        for file_column, style in enumerate(["solid", "dashed", "dotted"]):
            array = get_array(filename)
            axs[axis].plot(np.log10(array[:,0]), array[:,file_column+1], linestyle=style, color=color)
        axs[axis].set_xlim(6, 9)
        axs[axis].tick_params(direction="in")

    plot_file((0, 0), f"data/colors/b_v/{law}/bv_{law_f}_a.dat", "cornflowerblue")
    plot_file((0, 0), f"data/colors/b_v/{law}/bv_{law_f}_e.dat", "crimson")
    axs[0, 0].set_ylim(-0.2, 0.3)
    axs[0, 0].invert_yaxis()
    axs[0, 0].set_title("(B-V)")

    plot_file((0, 1), f"data/colors/u_b/{law}/ub_{law_f}_a.dat", "cornflowerblue")
    plot_file((0, 1), f"data/colors/u_b/{law}/ub_{law_f}_e.dat", "crimson")
    axs[0, 1].set_ylim(-1.5, 0)
    axs[0, 1].invert_yaxis()
    axs[0, 1].set_title("(U-B)")

    plot_file((1, 0), f"data/halpha_width/{law}/wha_{law_f}_a.dat", "cornflowerblue")
    plot_file((1, 0), f"data/halpha_width/{law}/wha_{law_f}_e.dat", "crimson")
    axs[1, 0].set_ylim(1, 4)
    axs[1, 0].set_title(r"Largeur équivalente de H$\alpha$")

    plot_file((2, 0), f"data/photon_number/below_228/{law}/228_{law_f}_a.dat", "cornflowerblue")
    plot_file((2, 0), f"data/photon_number/below_228/{law}/228_{law_f}_e.dat", "crimson")
    axs[2, 0].set_ylim(46, 51)
    axs[2, 0].set_title(r"Nombre de photons sous 228 $\AA$")

    plot_file((2, 1), f"data/photon_number/below_912/{law}/912_{law_f}_a.dat", "cornflowerblue")
    plot_file((2, 1), f"data/photon_number/below_912/{law}/912_{law_f}_e.dat", "crimson")
    axs[2, 1].set_ylim(51, 54)
    axs[2, 1].set_title(r"Nombre de photons sous 912 $\AA$")

    axs[0, 0].set_ylabel("indice de couleur [-]")
    axs[1, 0].set_ylabel(r"log (W(H$\alpha$) [$\AA$])")
    axs[2, 0].set_ylabel(r"log (N(H$^\degree$) [photons s$^{-1}$])")
    fig.supxlabel("log (Time [yr])")

    axs[1, 1].axis("off")

    fig.legend(handles=[
        mpatches.Patch(color="cornflowerblue", label=r"$Z=0.040$"),
        mpatches.Patch(color="crimson", label=r"$Z=0.001$"),
        mlines.Line2D([], [], color="black", linestyle="solid",  label=r"$\alpha=2.35$, $M_{up}=100\rm\ M_{\odot}$"),
        mlines.Line2D([], [], color="black", linestyle="dashed", label=r"$\alpha=3.30$, $M_{up}=100\rm\ M_{\odot}$"),
        mlines.Line2D([], [], color="black", linestyle="dotted", label=r"$\alpha=2.35$, $M_{up}=30\rm\ M_{\odot}$")
    ], loc=(0.5755,0.43), prop={'size': 12}
    )

    plt.tight_layout()
    plt.show()


make_5_panel_figure("continuous")
make_5_panel_figure("instantaneous")
