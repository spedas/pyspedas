from matplotlib import pyplot as plt

def save_plot(save_png=None, save_eps=None, save_svg=None, save_pdf=None, save_jpeg=None, dpi=300):

    if save_png is not None and save_png != '':
        if not save_png.endswith('.png'):
            save_png += '.png'
        plt.savefig(save_png, dpi=dpi)

    if save_eps is not None and save_eps != '':
        if not save_eps.endswith('.eps'):
            save_eps += '.eps'
        plt.savefig(save_eps, dpi=dpi)

    if save_svg is not None and save_svg != '':
        if not save_svg.endswith('.svg'):
            save_svg += '.svg'
        plt.savefig(save_svg, dpi=dpi)

    if save_pdf is not None and save_pdf != '':
        if not save_pdf.endswith('.pdf'):
            save_pdf += '.pdf'
        plt.savefig(save_pdf, dpi=dpi)

    if save_jpeg is not None and save_jpeg != '':
        if not save_jpeg.endswith('.jpeg'):
            save_jpeg += '.jpeg'
        plt.savefig(save_jpeg, dpi=dpi)
