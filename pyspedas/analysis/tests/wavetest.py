"""
This is a python version of the wavetest.pro script in IDL SPEDAS.
It is an example program for wavelet analysis using NINO3 SST dataset.
This script assumes that the data file sst_nino3.dat is in the same directory as the script.

Reference: Torrence, C. and G. P. Compo, 1998: A Practical Guide to
           Wavelet Analysis. <I>Bull. Amer. Meteor. Soc.</I>, 79, 61-78.

See also: wavelet98.py
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from pyspedas import wavelet98, wave_signif
from pyspedas.utilities.config_testing import TESTING_CONFIG, test_data_download_file

# Whether to display plots during testing
global_display = TESTING_CONFIG["global_display"]
# Directory to save testing output files
output_dir = TESTING_CONFIG["local_testing_dir"]
# Ensure output directory exists
analysis_dir = "analysis_tools"
save_dir = os.path.join(output_dir, analysis_dir)
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
# Directory with IDL SPEDAS validation files
validation_dir = TESTING_CONFIG["remote_validation_dir"]


def wavetest(noplot=False):
    """
    Python translation of wavetest.pro
    Wavelet analysis of NINO3 SST dataset.
    """

    # Download tplot files
    # The SPEDAS script that creates the file: general/tools/python_validate/wavelet_python_validate.pro

    data_file = test_data_download_file(
        validation_dir, analysis_dir, "sst_nino3.dat", save_dir
    )

    # Check if data file exists
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file not found: {data_file}")

    # Load SST time series data
    sst = np.loadtxt(data_file)
    n = len(sst)

    # Normalize by standard deviation (not necessary)
    sst = sst - np.mean(sst)

    # Parameters
    # dt: Time step (quarterly data)
    # xrange: Plotting range
    # pad: Padding for wavelet transform
    # s0: Start scale (3 months)
    # dj: Sub-octaves per octave
    # mother: Mother wavelet type
    dt = 0.25  # quarterly data
    time = np.arange(n) * dt + 1871.0
    xrange = [1870, 2000]

    # Wavelet parameters
    pad = 1
    s0 = dt  # start at scale of 3 months
    dj = 0.25  # 4 sub-octaves per octave
    j1 = 9.0 / dj  # this says do 9 powers-of-two with dj sub-octaves each
    mother = "MORLET"

    # Perform wavelet transform
    print("Computing wavelet transform...")
    wave, scale, period, signif, daughter_ret, sst_recon, fft_theor_out = wavelet98(
        sst, dt, pad=pad, dj=dj, j_scales=j1, s0=s0, mother=mother, recon=True
    )
    power = np.abs(wave) ** 2  # Wavelet power spectrum

    # Global wavelet spectrum (GWS) [Eqn(10)]
    global_ws = np.mean(power, axis=0)

    # Compute significance levels for the global wavelet spectrum
    # This corresponds to the IDL code:
    # global_signif = WAVE_SIGNIF(sst, dt, scale, 1, LAG1=0.0, DOF=dof, MOTHER=mother, CDELTA=Cdelta, PSI0=psi0)
    dof = len(sst) - scale  # Degrees of freedom
    global_signif, wave_outputs = wave_signif(
        sst, dt, scale, 1, lag1=0.0, dof=dof, mother=mother
    )
    Cdelta = wave_outputs["Cdelta"]

    # Add cone of influence (COI) for the wavelet power spectrum
    # This corresponds to the IDL code:
    # x = [time[0], time, MAX(time)]
    # y = [MAX(period), coi, MAX(period)]
    # POLYFILL, x, y, ORIEN=+45, SPACING=0.5, COLOR=color, NOCLIP=0, THICK=1
    coi = period / np.sqrt(2)  # Calculate COI based on wavelet period
    # Interpolate COI to match the length of the time array
    coi_interp = np.interp(time, time[: len(coi)], coi)
    if not noplot:
        plt.fill_between(
            time, coi_interp, np.max(period), color="white", alpha=0.7, hatch="///"
        )

    # Reconstruction variance (Parseval's theorem) [Eqn(14)]
    # Adjust scale shape for broadcasting
    recon_variance = (
        dj * dt / (np.sum(scale) * len(sst)) * np.sum(power / scale[None, :])
    )
    print(f"Reconstructed variance = {recon_variance:.4f} degC^2")

    # Additional reconstruction analysis if sst_recon is available
    if sst_recon is not None and len(sst_recon) > 1:
        # Calculate variance of reconstructed time series
        recon_variance_actual = np.var(
            sst_recon, ddof=0
        )  # Use population variance like IDL MOMENT

        # RMS of Reconstruction [Eqn(11)]
        rms_error = np.sqrt(np.sum((sst - sst_recon) ** 2) / n)

        # Original variance
        original_variance = np.var(
            sst, ddof=0
        )  # Use population variance like IDL MOMENT

        print()
        print("        ******** RECONSTRUCTION ********")
        print(f"original variance = {original_variance:.6f} degC^2")
        print(f"reconstructed var = {recon_variance_actual:.6f} degC^2")
        print(f"Ratio = {recon_variance_actual/original_variance:.6f}")
        print(f"root-mean-square error of reconstructed sst = {rms_error:.6f} degC")
        print()
        if mother.upper() == "DOG":
            print("Note: for better reconstruction with the DOG, you need")
            print("      to use a very small s0.")
        print()

    # RMS of Reconstruction [Eqn(11)] - original calculation
    rms_error = np.sqrt(np.mean((sst - np.mean(sst)) ** 2))
    print(
        f"RMS error of reconstruction = {rms_error:.4f}"
    )  # Keep original for compatibility

    # Compute scale-average between 2-8 years [Eqn(24)]
    # Following IDL implementation more closely
    avg_idx = np.where((period >= 2) & (period < 8))[0]
    if len(avg_idx) > 0:
        # Normalize power by scale (like IDL power_norm = power/scale_avg)
        scale_expanded = scale[None, :]  # Expand for broadcasting
        power_norm = power / scale_expanded

        # Scale-average calculation [Eqn(24)] - matches IDL exactly
        scale_avg = dj * dt / Cdelta * np.sum(power_norm[:, avg_idx], axis=1)
    else:
        scale_avg = np.zeros(len(time))

    # Compute scale-average significance levels
    # This corresponds to the IDL code:
    # scaleavg_signif = WAVE_SIGNIF(sst, dt, scale, 2, GWS=global_ws, SIGLVL=0.90, DOF=[2,7.9], MOTHER=mother)
    scaleavg_signif, _ = wave_signif(
        sst, dt, scale, 2, gws=global_ws, siglvl=0.90, dof=[2, 7.9], mother=mother
    )

    # Ensure scaleavg_signif matches the length of time
    if np.isscalar(scaleavg_signif):
        scaleavg_signif = np.full_like(time, scaleavg_signif, dtype=np.float64)
    elif len(scaleavg_signif) == 1:
        scaleavg_signif = np.full_like(time, scaleavg_signif[0], dtype=np.float64)

    # Plotting
    if not noplot:
        create_wavelet_plot(
            time,
            sst,
            time,
            period,
            power,
            global_ws,
            scale_avg,
            xrange,
            global_signif,
            scaleavg_signif,
        )

    print("\nWavelet analysis completed!")
    return {
        "time": time,
        "sst": sst,
        "period": period,
        "power": power,
        "global_ws": global_ws,
        "scale_avg": scale_avg,
    }


def create_wavelet_plot(
    time,
    sst,
    time_wv,
    period,
    power,
    global_ws,
    scale_avg,
    xrange,
    global_signif,
    scaleavg_signif,
):
    """
    Create the wavelet analysis plot similar to IDL version
    """

    fig = plt.figure(figsize=(12, 10))

    # Plot 1: Time series (top panel, full width)
    _ = plt.subplot2grid((4, 4), (0, 0), colspan=3)
    plt.plot(time, sst, "b-", linewidth=1)
    plt.xlim(xrange)
    plt.xlabel("Time (year)")
    plt.ylabel("NINO3 SST (°C)")
    plt.title("a) NINO3 Sea Surface Temperature (seasonal)")
    plt.grid(True, alpha=0.3)

    # Adjust subplot positioning to give more space for labels and prevent overlap
    plt.subplots_adjust(
        left=0.12, bottom=0.08, right=0.95, top=0.95, hspace=0.4, wspace=0.3
    )

    # Plot 2: Wavelet power spectrum (middle left, 3/4 width)
    _ = plt.subplot2grid((4, 4), (1, 0), colspan=3, rowspan=2)

    # Create contour plot with IDL-like styling
    levels = [0.5, 1, 2, 4]  # Contour levels for power spectrum
    colors = ["lightblue", "yellow", "orange", "red"]

    X, Y = np.meshgrid(time_wv, period)
    _ = plt.contourf(X, Y, power.T, levels=levels, colors=colors, extend="max")

    # Cone of influence (placeholder)
    coi = np.max(period) * np.ones_like(time_wv)  # Placeholder for COI calculation
    plt.fill_between(
        time_wv, coi, np.max(period), color="white", alpha=0.7, hatch="///"
    )

    plt.xlim(xrange)
    plt.ylim([128, 0.5])  # Extended range like requested (128 at top, 0.5 at bottom)
    plt.yscale("log")
    # Create powers-of-2 ticks like IDL
    yticks = [0.5, 1, 2, 4, 8, 16, 32, 64, 128]
    plt.yticks(yticks, [str(int(y)) if y >= 1 else str(y) for y in yticks])
    plt.xlabel("Time (year)")
    plt.ylabel("Period (years)")
    plt.title("b) Wavelet Power Spectrum (contours at 0.5,1,2,4°C²)")

    # Plot 3: Global wavelet spectrum (middle right, 1/4 width)
    ax3 = plt.subplot2grid((4, 4), (1, 3), rowspan=2)
    plt.plot(global_ws, period, "b-", linewidth=2)
    plt.plot(global_signif, period, "r--", linewidth=1)
    # Linear scales but inverted like plot 2
    plt.xlim([0, 4])  # Linear x-axis from 0 to 4
    plt.ylim([128, 0.5])  # Same inverted range as plot 2 but linear
    plt.yscale("log")
    ax3.set_yscale("log")  # Explicitly set y-axis to linear using axes object
    # Use same tick positions as plot 2 but no labels
    yticks = [0.5, 1, 2, 4, 8, 16, 32, 64, 128]
    plt.yticks(yticks, [""] * len(yticks))
    plt.xlabel("Power (°C²)")
    plt.title("c) Global")
    plt.text(0.7, 0.8, "95%", transform=ax3.transAxes)
    plt.grid(True, alpha=0.3)

    # Plot 4: Scale-average time series (bottom panel, 3/4 width)
    _ = plt.subplot2grid((4, 4), (3, 0), colspan=3)
    plt.plot(time_wv, scale_avg, "b-", linewidth=2)
    # Plot significance as horizontal line
    if np.isscalar(scaleavg_signif):
        plt.axhline(y=scaleavg_signif, color="r", linestyle="--", linewidth=1)
    else:
        plt.plot(time_wv, scaleavg_signif, "r--", linewidth=1)
    plt.xlim(xrange)
    plt.ylim([0, np.max(scale_avg) * 1.25])  # Auto-scale like IDL
    plt.xlabel("Time (year)")
    plt.ylabel("Avg variance (°C²)")
    plt.title("d) 2-8 yr Scale-average Time Series")
    plt.grid(True, alpha=0.3)

    # Save figure to output directory and then show it (optionally)
    output_path = os.path.join(save_dir, "wavelet_analysis_nino3_sst.png")
    fig.savefig(output_path, dpi=300, facecolor="white")
    if global_display:
        plt.show()


if __name__ == "__main__":
    # Run the wavelet test
    result = wavetest()
