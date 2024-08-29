import logging
import pyspedas
from pyspedas.projects.mms import fgm, fpi, feeps, hpca, edp, eis
from pyspedas.projects.themis import gmag
from pytplot import options, tplot_options, store_data, tplot, tnames, time_double, time_string


def mms_overview_plot(
    trange=[],
    date="2022-03-23",
    duration="1",
    probe="1",
    skip_ae_idx=False,
    save_png='',
    save_eps='',
    save_svg='',
    save_pdf='',
    save_jpeg='',
    display=True,
    xsize=10,
    ysize=14,
):
    r"""
    Generate an overview plot for MMS data.

    Parameters:
    -----------
    trange (list of 2 strings, optional):
        Time range, start and end date. If not specified, it will be calculated based on the date and duration parameters.
    date: str, optional
        Date in the format 'YYYY-MM-DD' or 'YYY-MM-DD/hh:mm:ss. Used to calculate the time range if trange is not specified.
    duration: str, optional
        Duration in days. Used to calculate the time range if trange is not specified.
    probe: str, optional
        MMS probe number (1-4).
    skip_ae_idx: bool, optional
        Whether to skip plotting the AE index panel.
    save_png: str, optional
        .Filename to save plot as PNG
    save_eps: str, optional
        .Filename to save plot as EPS
    save_svg: str, optional
        .Filename to save plot as SVG
    save_pdf: str, optional
        .Filename to save plot as PDF
    save_jpeg: str, optional
        .Filename to save plot as JPEG
    display: bool, optional
        If True, then this function will display the plotted tplot variables. Necessary to make this optional
        so we can avoid it in a headless server environment.
    xsize: int, optional
        Size of the x-axis of the plot window in inches. Default is 10.
    ysize: int, optional
        Size of the y-axis of the plot window in inches. Default is 14.

    Returns:
    --------
    None

    Examples:
    ---------
    from pyspedas import mms_overview_plot
    mms_overview_plot(date='2023-03-23', probe='1', save_png="c:\\work\\mms\\summary_plots\mms_overview", display=False)

    Notes:
    ------
    It may need a long time to complete.

    Todo:
    -----
    1. Implement time_clip. Currently, it is not working correctly for spectra.
    2. Fix legends. The option "legend_location"="spedas", does not work correctly, it hides part of the legend, both on screen and in the saved PNG file.
    3. Implement thm_gen_multipngplot (6 hours, 2 hours).
    4. Fix problems when data is missing.
    """

    # If trange is not specified, use date and duration
    if (
        isinstance(trange, list)
        and len(trange) == 2
        and isinstance(trange[0], str)
        and isinstance(trange[1], str)
    ):
        t1 = time_double(trange[0])
        t2 = time_double(trange[1])
        trange = [t1, t2]
    else:
        t1 = time_double(date)
        t2 = t1 + float(duration) * 86400.0
        trange = [t1, t2]

    time_clip_value = False

    # Empty panel
    store_data("empty_panel", data={"x": trange, "y": [0, 0]})

    # Panel 1: AE index
    panel01 = "thg_idx_combined"
    if not skip_ae_idx:
        gmag(sites="idx", trange=trange, time_clip=time_clip_value)
        d1_1 = "thg_idx_ae"
        d1_2 = "thg_idx_uc_avg"

        store_data(panel01, data=[d1_1, d1_2])
        options(panel01, "name", "")
        options(panel01, "Color", ["black", "green"])
        options(panel01, "legend_names", ["Themis AE", "Kyoto proxy AE"])
        options(panel01, "ytitle", "AE Intex")
        options(panel01, "ysubtitle", "[nt]")
        options(panel01, "legend_location", "spedas")

    # Panel 2: FGM magnetic field mms_fpi_density
    panel02 = "mms" + probe + "_fgm_b_gsm_srvy_l2_bvec"
    fgm(trange=trange, probe=probe, data_rate="srvy", time_clip=time_clip_value)
    options(panel02, "ytitle", "FGM")
    options(panel02, "ysubtitle", "[nT]")
    options(panel02, "legend_location", "spedas")

    # Panel 3: EPD proton flux mms_epd_eis_extof_proton_flux_omni epd_eis_srvy_l2_extof_proton_flux_omni
    panel03 = "mms" + probe + "_epd_eis_srvy_l2_extof_proton_flux_omni"
    eis(
        trange=trange,
        probe=probe,
        datatype="extof",
        data_rate="srvy",
        time_clip=time_clip_value,
    )
    # options(panel03, "ytitle", "EPD\nEIS\nProton\nenergy")
    options(panel03, "ytitle", "EPD EIS\nProton energy")
    options(panel03, "ysubtitle", "[keV]")
    options(panel03, "legend_location", "spedas")

    # Panel 4: DIS Energy spectrogram mms_dis_energyspectr_omni_fast
    panel04 = "mms" + probe + "_dis_energyspectr_omni_fast"
    fpi(
        trange=trange,
        probe=probe,
        datatype=["des-moms", "dis-moms"],
        time_clip=time_clip_value,
    )
    options(panel04, "ytitle", "DIS\nenergy\nomni fast")
    options(panel04, "ysubtitle", "[eV]")
    options(panel04, "legend_location", "spedas")

    # Panel 5: Electron intensity mms_epd_feeps_srvy_l2_electron_intensity_omni
    panel05 = "mms" + probe + "_epd_feeps_srvy_l2_electron_intensity_omni"
    feeps(trange=trange, probe=probe, time_clip=time_clip_value)
    options(panel05, "ytitle", "Electron\nintensity\nomni")
    options(panel05, "ysubtitle", "[keV]")
    options(panel05, "legend_location", "spedas")

    # Panel 6: DES Energy spectrogram mms_des_energyspectr_omni_fast
    panel06 = "mms" + probe + "_des_energyspectr_omni_fast"
    options(panel06, "ytitle", "DES\nenergy\nomni fast")
    options(panel06, "ysubtitle", "[eV]")
    options(panel06, "legend_location", "spedas")

    # Panel 7: HPCA H- density mms_hpca_hplus_number_density
    panel07 = "mms" + probe + "_hpca_hplus_number_density"
    hpca(trange=trange, probe=probe, time_clip=time_clip_value)
    options(panel07, "ytitle", "HPCA\nH- density")
    options(panel07, "ysubtitle", "[cm-3]")
    options(panel07, "Color", ["blue"])
    options(panel07, "legend_location", "spedas")

    # Panel 8: EDP mms_edp_dce_dsl_fast_l2
    panel08 = "mms" + probe + "_edp_dce_dsl_fast_l2"
    edp(trange=trange, probe=probe, time_clip=time_clip_value)
    options(panel08, "ytitle", "EDP\nE Field")
    options(panel08, "ysubtitle", "[mV/m]")
    options(panel08, "legend_location", "spedas")

    # Panel 9: mms_fpi_density
    panel09 = "mms" + probe + "_fpi_density"
    d8_1 = "mms" + probe + "_dis_numberdensity_fast"
    d8_2 = "mms" + probe + "_des_numberdensity_fast"
    if tnames(d8_1) != [] and tnames(d8_2) != []:
        store_data(panel09, data=[d8_1, d8_2])
        options(panel09, "Color", ["green", "blue"])
        options(panel09, "legend_names", ["Ni, ions", "Ne, electrons"])
    elif tnames(d8_1) == [] and tnames(d8_2) == []:
        panel09 = "empty_panel"
    elif tnames(d8_1) == []:
        panel09 = d8_2
        options(panel09, "Color", ["blue"])
        options(panel09, "legend_names", ["Ne, electrons"])
    elif tnames(d8_2) == []:
        panel09 = d8_1
        options(panel09, "Color", ["green"])
        options(panel09, "legend_names", ["Ni, ions"])
    options(panel09, "name", "")
    options(panel09, "ytitle", "DIS")
    options(panel09, "ysubtitle", "[cm^-3]")
    options(panel09, "legend_location", "spedas")

    # Panel 10: HPCA H+ velocity mms_hpca_hplus_ion_bulk_velocity_GSM
    panel10 = "mms" + probe + "_hpca_hplus_ion_bulk_velocity_GSM"
    options(panel10, "ytitle", "HPCA\nH+ vel")
    options(panel10, "ysubtitle", "[km/s]")
    options(panel10, "legend_names", ["Vx(H^+)", "Vy(H^+)", "Vz(H^+)"])
    options(panel10, "legend_location", "spedas")

    # Panel 11: HPCA O- velocity mms_hpca_oplus_ion_bulk_velocity_GSM
    panel11 = "mms" + probe + "_hpca_oplus_ion_bulk_velocity_GSM"
    options(panel11, "ytitle", "HPCA\nO+ vel")
    options(panel11, "ysubtitle", "[km/s]")
    options(panel11, "legend_names", ["Vx(O^+)", "Vy(O^+)", "Vz(O^+)"])
    options(panel11, "legend_location", "spedas")

    # Save plot
    fname = None
    if isinstance(t1, str):
        t0 = time_string(time_double(t1), fmt="%Y_%m_%d")
    else:
        t0 = time_string(t1, fmt="%Y_%m_%d")

    # Full plot
    vars = [
        panel02,
        panel03,
        panel04,
        panel05,
        panel06,
        panel07,
        panel08,
        panel09,
        panel10,
        panel11,
    ]

    if not skip_ae_idx:
        vars.insert(0, panel01)

    # time_clip(vars, time_start=trange[0], time_end=trange[1])
    plot_title = "MMS-" + probe + " Overview (" + t0.replace("_", "-") + ")"
    tplot_options("title", plot_title)
    options(panel01, "name", plot_title)
    # tplot_options("wsize", [1400, 1000]) does not work
    tplot_options("show_all_axes", False)
    xsize = int(xsize)
    ysize = int(ysize)

    tplot(vars, save_png=save_png,save_eps=save_eps,save_svg=save_svg,save_pdf=save_pdf,save_jpeg=save_jpeg, display=display, xsize=xsize, ysize=ysize)
    logging.info("MMS overview plot completed.")
