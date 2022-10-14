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
         colormap=None,
         olines=8,
         contours=False,
         plotsize=10,
         save_png=None,
         save_jpeg=None,
         save_svg=None,
         save_pdf=None,
         save_eps=None,
         dpi=None,
         display=True):
    """
    Creates plots of 2D particle slices
    """
    spec_options = {}

    if zrange is None:
        zrange = the_slice.get('zrange')
        # padding, # in thm_ui_slice2d should match this
        zrange = [zrange[0]*0.999, zrange[1]*1.001]

    if zrange is None:
        spec_options['norm'] = mpl.colors.LogNorm()
    else:
        spec_options['norm'] = mpl.colors.LogNorm(vmin=zrange[0], vmax=zrange[1])

    style = pytplot.tplot_opt_glob.get('style')

    if style is None:
        if colormap is None:
            colormap = 'spedas'
    else:
        plt.style.use(style)

    if colormap == 'spedas':
        _colors = pytplot.spedas_colorbar
        spd_map = [(np.array([r, g, b])).astype(np.float64) / 256 for r, g, b in zip(_colors.r, _colors.g, _colors.b)]
        cmap = LinearSegmentedColormap.from_list('spedas', spd_map)
    else:
        cmap = colormap

    spec_options['cmap'] = cmap

    char_size = pytplot.tplot_opt_glob.get('charsize')
    if char_size is None:
        char_size = 12

    fig, axes = plt.subplots()
    fig.set_size_inches(plotsize, plotsize)

    if xrange is not None:
        axes.set_xlim(xrange)

    if yrange is not None:
        axes.set_ylim(yrange)

    axis_font_size = pytplot.tplot_opt_glob.get('axis_font_size')

    if axis_font_size is not None:
        axes.tick_params(axis='x', labelsize=axis_font_size)
        axes.tick_params(axis='y', labelsize=axis_font_size)

    info = slice2d_getinfo(the_slice)

    axes.set_title(info['title'], fontsize=char_size)
    axes.set_ylabel(info['ytitle'], fontsize=char_size)
    axes.set_xlabel(info['xtitle'], fontsize=char_size)

    fig.subplots_adjust(left=0.14, right=0.86, top=0.86, bottom=0.14)

    box = axes.get_position()
    pad, width = 0.02, 0.01
    cax = fig.add_axes([box.xmax + pad, box.ymin, width, box.height])

    if axis_font_size is not None:
        cax.tick_params(labelsize=axis_font_size)

    im = axes.pcolormesh(the_slice['xgrid'], the_slice['ygrid'], the_slice['data'].T, **spec_options)

    colorbar = fig.colorbar(im, cax=cax)

    colorbar.set_label(info['ztitle'], fontsize=char_size)

    # draw lines at the origin
    axes.axvline(x=0, linestyle=(0, (5, 10)), color='black')
    axes.axhline(y=0, linestyle=(0, (5, 10)), color='black')

    interp_type = the_slice.get('interpolation')

    if interp_type != 'geometric' or contours:
        levels = 10.**(np.arange(olines)/float(olines)*(np.log10(zrange[1])-np.log10(zrange[0]))+np.log10(zrange[0]))
        contours = axes.contour(the_slice['xgrid'], the_slice['ygrid'], the_slice['data'].T, levels, linewidths=0.5)

    if save_png is not None and save_png != '':
        plt.savefig(save_png + '.png', dpi=dpi)

    if save_jpeg is not None and save_jpeg != '':
        plt.savefig(save_jpeg + '.jpeg', dpi=dpi)

    if save_eps is not None and save_eps != '':
        plt.savefig(save_eps + '.eps', dpi=dpi)

    if save_svg is not None and save_svg != '':
        plt.savefig(save_svg + '.svg', dpi=dpi)

    if save_pdf is not None and save_pdf != '':
        plt.savefig(save_pdf + '.pdf', dpi=dpi)

    if display:
        plt.show()
