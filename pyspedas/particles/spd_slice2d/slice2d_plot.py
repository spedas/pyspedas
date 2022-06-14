import pytplot
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from .slice2d_getinfo import slice2d_getinfo


def plot(the_slice,
         xrange=None,
         yrange=None,
         zrange=None,
         plotsize=10,
         save_png=None,
         save_svg=None,
         save_pdf=None,
         save_eps=None,
         display=True):
    """

    """
    spec_options = {}

    if zrange is None:
        spec_options['norm'] = mpl.colors.LogNorm()
    else:
        spec_options['norm'] = mpl.colors.LogNorm(vmin=zrange[0], vmax=zrange[1])

    _colors = pytplot.spedas_colorbar
    spd_map = [(np.array([r, g, b])).astype(np.float64) / 256 for r, g, b in zip(_colors.r, _colors.g, _colors.b)]
    cmap = LinearSegmentedColormap.from_list('spedas', spd_map)
    spec_options['cmap'] = cmap

    fig, axes = plt.subplots()
    fig.set_size_inches(plotsize, plotsize)

    if xrange is not None:
        axes.set_xlim(xrange)

    if yrange is not None:
        axes.set_ylim(yrange)

    info = slice2d_getinfo(the_slice)

    axes.set_title(info['title'])
    axes.set_ylabel(info['ytitle'])
    axes.set_xlabel(info['xtitle'])

    box = axes.get_position()
    pad, width = 0.02, 0.01
    cax = fig.add_axes([box.xmax + pad, box.ymin, width, box.height])

    im = axes.pcolormesh(the_slice['xgrid'], the_slice['ygrid'], the_slice['data'].T, **spec_options)

    colorbar = fig.colorbar(im, cax=cax)

    colorbar.set_label(info['ztitle'])

    # draw lines at the origin
    axes.axvline(x=0, linestyle=(0, (5, 10)), color='black')
    axes.axhline(y=0, linestyle=(0, (5, 10)), color='black')

    if save_png is not None and save_png != '':
        plt.savefig(save_png + '.png')

    if save_eps is not None and save_eps != '':
        plt.savefig(save_eps + '.eps')

    if save_svg is not None and save_svg != '':
        plt.savefig(save_svg + '.svg')

    if save_pdf is not None and save_pdf != '':
        plt.savefig(save_pdf + '.pdf')

    if display:
        plt.show()
