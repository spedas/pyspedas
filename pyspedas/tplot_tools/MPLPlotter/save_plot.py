from matplotlib import pyplot as plt
from pathlib import Path

from pyspedas.config import CONFIG


def _plot_filename(filename):
    """Resolve bare plot filenames under the configured plot directory."""
    path = Path(filename).expanduser()
    if not path.is_absolute() and path.parent == Path("."):
        path = Path(CONFIG["plotting"]["plot_directory"]).expanduser() / path
        path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)

def save_plot(save_png=None, save_eps=None, save_svg=None, save_pdf=None, save_jpeg=None, dpi=300):

    if save_png is not None and save_png != '':
        if not save_png.endswith('.png'):
            save_png += '.png'
        plt.savefig(_plot_filename(save_png), dpi=dpi)

    if save_eps is not None and save_eps != '':
        if not save_eps.endswith('.eps'):
            save_eps += '.eps'
        plt.savefig(_plot_filename(save_eps), dpi=dpi)

    if save_svg is not None and save_svg != '':
        if not save_svg.endswith('.svg'):
            save_svg += '.svg'
        plt.savefig(_plot_filename(save_svg), dpi=dpi)

    if save_pdf is not None and save_pdf != '':
        if not save_pdf.endswith('.pdf'):
            save_pdf += '.pdf'
        plt.savefig(_plot_filename(save_pdf), dpi=dpi)

    if save_jpeg is not None and save_jpeg != '':
        if not save_jpeg.endswith('.jpeg'):
            save_jpeg += '.jpeg'
        plt.savefig(_plot_filename(save_jpeg), dpi=dpi)
