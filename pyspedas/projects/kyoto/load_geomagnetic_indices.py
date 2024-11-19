import logging
from .load_dst import dst as load_dst
from .load_ae import load_ae
from pyspedas.projects.themis.ground.gmag import gmag as thm_gmag
from pyspedas.projects.noaa.noaa_load_kp import noaa_load_kp
from pyspedas.projects.omni import data as omni_load
from pytplot import time_clip as tclip


def load_geomagnetic_indices(
    datatypes=None,
    omni_load_all=False,
    missions=["kyoto", "themis", "noaa", "gfz", "omni"],
    trange=["2024-05-11 00:00:00", "2024-05-11 23:59:59"],
    prefix="",
    suffix="",
    force_download=False,
    time_clip=True,
):
    """
    Loads geomagnetic indices data from different sources.

    Kyoto: ["dst", "ae", "al", "ao", "au", "ax"]
    Themis: ['thg_idx_al', 'thg_idx_au', 'thg_idx_ae', 'thg_idx_uc_al', 'thg_idx_uc_au', 'thg_idx_uc_ae', 'thg_idx_uc_avg']
    NOAA or gfz: ['Kp', 'ap', 'Sol_Rot_Num', 'Sol_Rot_Day', 'Kp_Sum', 'ap_Mean', 'Cp', 'C9', 'Sunspot_Number', 'F10.7', 'Flux_Qualifier']
    Omni: ['AE_INDEX', 'AL_INDEX', 'AU_INDEX', 'SYM_D', 'SYM_H', 'ASY_D', 'ASY_H', 'Pressure']

    Parameters
    ----------
    datatypes : list, optional
        A list of strings specifying the types of geomagnetic indices to load.
        Default is None, which downloads all available indices from the specified missions.
    missions : list, optional
        A list of strings specifying the data missions to load the indices from.
        Default is ["kyoto", "themis", "noaa", "omni"].
    omni_load_all : bool, optional
        A boolean indicating whether to load all available variables from the Omni data.
        Default is False.
    trange : list or tuple, optional
        A list specifying the time range of the data to load.
        Default is ["2024-05-11 00:00:00", "2024-05-11 23:59:59"].
    prefix : str, optional
        A string to prepend to the variable names when loading the data.
        Default is an empty string.
    suffix : str, optional
        A string to append to the variable names when loading the data.
        Default is an empty string.
    force_download : bool, optional
        A boolean specifying whether to force the data to be downloaded,
        even if the data already exists locally.
        Default is False.
    time_clip : bool, optional
        A boolean specifying whether to clip the data to the specified time range.
        Default is True.

    Returns
    -------
    List of str
        A list of tplot variable names that were loaded.

    """
    vars = []  # list of tplot variables to return

    if datatypes is None or datatypes == [] or "*" in datatypes:
        datatypes = None

    if trange is None or len(trange) != 2:
        logging.error("Keyword trange with two datetimes is required to download data.")
        return vars
    if trange[0] >= trange[1]:
        logging.error("Invalid time range. End time must be greater than start time.")
        return vars

    missions = [missions] if isinstance(missions, str) else missions

    for p in missions:
        p = p.lower()
        if p == "kyoto":
            if datatypes is None or "dst" in datatypes:
                dst_vars = load_dst(
                    trange=trange,
                    prefix=prefix,
                    suffix=suffix,
                    time_clip=time_clip,
                    force_download=force_download,
                )
                if len(dst_vars) < 1:
                    logging.info("No Kyoto Dst data found.")
                else:
                    vars.extend(dst_vars)
            if datatypes is not None and "dst" in datatypes:
                datatypes.remove("dst")

            if datatypes is None:
                ae_vars = load_ae(
                    trange=trange,
                    prefix=prefix,
                    suffix=suffix,
                    time_clip=time_clip,
                    force_download=force_download,
                )
                if len(ae_vars) < 1:
                    logging.info("No Kyoto AE data found.")
                else:
                    vars.extend(ae_vars)
            else:
                ae_vars = load_ae(
                    trange=trange,
                    datatypes=datatypes,
                    prefix=prefix,
                    suffix=suffix,
                    time_clip=time_clip,
                    force_download=force_download,
                )
                if len(ae_vars) < 1:
                    logging.info("No Kyoto AE data found.")
                else:
                    vars.extend(ae_vars)
        elif p == "themis":
            # Todo: currently, gmag does not support prefix
            if datatypes is None:
                thm_vars = thm_gmag(
                    trange=trange,
                    sites="idx",
                    prefix=prefix,
                    suffix=suffix,
                    time_clip=time_clip,
                    force_download=force_download,
                )
                if len(thm_vars) < 1:
                    logging.info("No THEMIS index data found.")
                else:
                    vars.extend(thm_vars)
            else:
                thm_vars = thm_gmag(
                    trange=trange,
                    sites="idx",
                    varnames=datatypes,
                    prefix=prefix,
                    suffix=suffix,
                    time_clip=time_clip,
                    force_download=force_download,
                )
                if len(thm_vars) < 1:
                    logging.info("No THEMIS index data found.")
                else:
                    vars.extend(thm_vars)
        elif p == "noaa":
            nprefix = prefix + "noaa_"  # NOAA data needs a prefix
            if datatypes is None:
                noaa_vars = noaa_load_kp(
                    trange=trange,
                    prefix=nprefix,
                    suffix=suffix,
                    time_clip=time_clip,
                    force_download=force_download,
                )
                if len(noaa_vars) < 1:
                    logging.info("No NOAA index data found.")
                else:
                    vars.extend(noaa_vars)
            else:
                noaa_vars = noaa_load_kp(
                    trange=trange,
                    datatype=datatypes,
                    prefix=nprefix,
                    suffix=suffix,
                    time_clip=time_clip,
                    force_download=force_download,
                    gfz=False,
                )
                if len(noaa_vars) < 1:
                    logging.info("No NOAA index data found.")
                else:
                    vars.extend(noaa_vars)
        elif p == "gfz":
            gprefix = prefix + "gfz_"  # GFZ data needs a prefix
            if datatypes is None:
                gfz_vars = noaa_load_kp(
                    trange=trange,
                    prefix=gprefix,
                    suffix=suffix,
                    time_clip=time_clip,
                    gfz=True,
                    force_download=force_download,
                )
                if len(gfz_vars) < 1:
                    logging.info("No GFZ index data found.")
                else:
                    vars.extend(gfz_vars)
            else:
                gfz_vars = noaa_load_kp(
                    trange=trange,
                    datatype=datatypes,
                    prefix=gprefix,
                    suffix=suffix,
                    time_clip=time_clip,
                    gfz=True,
                )
                if len(gfz_vars) < 1:
                    logging.info("No GFZ index data found.")
                else:
                    vars.extend(gfz_vars)
        elif p == "omni":
            oprefix = prefix + "omni_"  # Omni data needs a prefix
            if datatypes is None and not omni_load_all:
                # Omni loads too many variables, we need to restrict them
                odatatypes = [
                    "Pressure",
                    "AE_INDEX",
                    "AL_INDEX",
                    "AU_INDEX",
                    "SYM_D",
                    "SYM_H",
                    "ASY_D",
                    "ASY_H",
                ]
            else:
                odatatypes = ['IMF', 'PLS', 'IMF_PTS', 'PLS_PTS', 'percent_interp', 'Timeshift',
                    'RMS_Timeshift', 'RMS_phase', 'Time_btwn_obs', 'F', 'BX_GSE', 'BY_GSE', 'BZ_GSE',
                    'BY_GSM', 'BZ_GSM', 'RMS_SD_B', 'RMS_SD_fld_vec', 'flow_speed', 'Vx',  'Vy', 'Vz',
                    'proton_density', 'T','NaNp_Ratio', 'Pressure', 'E', 'Beta', 'Mach_num', 'Mgs_mach_num',
                    'x', 'y', 'z', 'BSN_x', 'BSN_y', 'BSN_z', 'AE_INDEX', 'AL_INDEX', 'AU_INDEX', 'SYM_D',
                     'SYM_H', 'ASY_D','ASY_H']
            omni_vars = omni_load(
                trange=trange,
                prefix=oprefix,
                suffix=suffix,
                time_clip=time_clip,
                varnames=odatatypes,
                force_download=force_download,
            )
            if len(omni_vars) < 1:
                logging.info("No Omni data found.")
            else:
                vars.extend(omni_vars)

    if time_clip:
        tclip(vars, trange[0], trange[1], overwrite=True)

    return vars
