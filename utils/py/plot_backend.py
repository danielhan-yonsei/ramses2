import matplotlib
import matplotlib.pyplot as plt

def set_backend(no_display=False):
    """Select a matplotlib backend that can actually be loaded.

    With no_display, use the non-interactive Agg backend (images can still
    be saved with savefig). Otherwise try the default GUI backend, then
    TkAgg, and fall back to Agg if neither is available (e.g. no Qt
    bindings installed, or no X display).

    Returns True if no GUI display is possible, so that plt.show() should
    be skipped.
    """
    if no_display:
        plt.switch_backend("Agg")
        return True
    for backend in [None, "TkAgg"]:
        try:
            plt.switch_backend(backend or matplotlib.rcParams["backend"])
            return False
        except ImportError:
            pass
    print("No GUI backend available: disabling display (use --out to save)")
    plt.switch_backend("Agg")
    return True
