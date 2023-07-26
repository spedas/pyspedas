import pyspedas
from pytplot import tplot_names
from pytplot import tplot, tplot_options, time_clip

if __name__ == '__main__':

    # data = pyspedas.elfin.state(trange=['2022-01-14/06:28', '2022-01-14/06:35'], probe='a')
    # tplot('ela_pos_gei')
    # breakpoint()

    epd_var = pyspedas.elfin.epd(trange=['2022-01-14/06:28', '2022-01-14/06:29'], probe='a')
    
    epd_var = pyspedas.elfin.epd(trange=['2022-01-14/06:28', '2022-01-14/06:29'], probe='a', type_='eflux')
    breakpoint()
    time_clip(
        ['ela_pef_nflux', 'ela_pef_sectnum','ela_pef_ns›pinsinsum','ela_pef_nsectors','ela_pef_spinper'], 
        '2022-01-14/06:28', '2022-01-14/06:29', overwrite=True)
    tplot(['ela_pef_nflux', 'ela_pef_eflux', 'ela_pef_sectnum','ela_pef_spinper'])
   