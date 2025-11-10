import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from IPython import display
import neurokit2 as nk
import os
import sys


def main(mat_file=r"example_data\02032000.mat"):
    # If mat_file is a relative path, resolve it relative to the script's directory
    if not os.path.isabs(mat_file):
        file_dir = os.getcwd()
        mat_file = os.path.join(file_dir, mat_file)
        mat_file = os.path.abspath(mat_file)  # Normalize the path
    
    if not os.path.exists(mat_file):
        print(f"Error: File not found: {mat_file}")
        return
    
    # --- Load file ---
    mat_data = sio.loadmat(mat_file)

    print(f"Loading mat file: {os.path.basename(mat_file)}")

    data = mat_data["data"]
    labels = ["".join(col).strip() for col in mat_data["labels"].astype(str)]
    units = ["".join(col).strip() for col in mat_data["units"].astype(str)]

    # --- Extract ISI and calculate sampling frequency ---
    isi = mat_data["isi"][0, 0]  # Extract scalar value
    isi_units = "".join(mat_data["isi_units"][0]).strip()  # Extract unit string

    print(f"\nISI: {isi} {isi_units}")

    # Convert ISI to seconds based on units
    if isi_units.lower() == "ms":
        isi_seconds = isi / 1000.0
    elif isi_units.lower() == "s":
        isi_seconds = isi
    elif isi_units.lower() == "us" or isi_units.lower() == "µs":
        isi_seconds = isi / 1000000.0
    else:
        isi_seconds = isi  # Assume seconds if unknown
        print(f"Warning: Unknown ISI unit '{isi_units}', assuming seconds")

    # Calculate sampling frequency (Hz)
    sampling_frequency = 1.0 / isi_seconds
    print(f"Sampling frequency: {sampling_frequency:.2f} Hz")

    # Calculate modifier to convert sample number to minutes
    # minutes = samples / (sampling_frequency * 60)
    samples_to_minutes = 1.0 / (sampling_frequency * 60.0)
    print(f"Sample-to-minutes conversion: {samples_to_minutes:.6f} minutes per sample")
    print(f"  (or: {1.0/samples_to_minutes:.2f} samples per minute)")

    # --- Helper function to find channel index ---
    def find_channel(label_list, keyword):
        for i, lbl in enumerate(label_list):
            if keyword.lower() in lbl.lower():
                return i
        return None

    # --- Identify channels by keyword ---
    idx_eda = find_channel(labels, "EDA")
    idx_ecg = find_channel(labels, "ECG")
    idx_trg = find_channel(labels, "Trigger")

    print("Indices:")
    print(" EDA:", idx_eda)
    print(" ECG:", idx_ecg)
    print(" Trigger:", idx_trg)

    # --- Extract signals ---
    eda = data[:, idx_eda] if idx_eda is not None else None
    ecg = data[:, idx_ecg] if idx_ecg is not None else None
    trigger = data[:, idx_trg] if idx_trg is not None else None
    eda_unit = units[idx_eda] if idx_eda is not None else ""
    ecg_unit = units[idx_ecg] if idx_ecg is not None else ""

    # --- NeuroKit2 preprocessing ---
    # EDA: tonic and phasic
    eda_signals, eda_info = nk.eda_process(eda, sampling_rate=sampling_frequency)
    avg_tonic = np.mean(eda_signals["EDA_Tonic"])
    avg_phasic = np.mean(eda_signals["EDA_Phasic"])

    # Phasic peaks: count detected SCR peaks
    num_peaks = np.sum(eda_signals["SCR_Peaks"] == 1)
    print(f"\nEDA - Average Tonic: {avg_tonic:.4f} {eda_unit}, Average Phasic: {avg_phasic:.4f} {eda_unit}")
    print(f"EDA - Number of SCR Peaks: {num_peaks}")

    # ECG: heart rate and quality
    ecg_signals, ecg_info = nk.ecg_process(ecg, sampling_rate=sampling_frequency)
    avg_hr = np.mean(ecg_signals["ECG_Rate"])

    # ECG SNR: signal (R-peak amplitude) / noise (baseline RMS)
    r_peaks = ecg_signals["ECG_R_Peaks"]
    if np.sum(r_peaks) > 0:
        signal_amplitude = np.mean(np.abs(ecg_signals["ECG_Clean"][r_peaks == 1]))
        noise_rms = np.sqrt(np.mean(ecg_signals["ECG_Clean"][r_peaks == 0]**2))
        snr_db = 20 * np.log10(signal_amplitude / noise_rms) if noise_rms > 0 else np.inf
        snr_status = "high" if snr_db > 20 else "low"
        print(f"ECG - Average HR: {avg_hr:.2f} bpm ({ecg_unit})")
        print(f"ECG - SNR: {snr_db:.2f} dB ({snr_status})")
    else:
        print(f"ECG - Average HR: {avg_hr:.2f} bpm ({ecg_unit})")
        print(f"ECG - SNR: Could not calculate (no R-peaks detected)")

    # --- Create time array in minutes ---
    num_samples = data.shape[0]
    time_minutes = np.arange(num_samples) * samples_to_minutes

    # --- Plot all three ---
    plt.figure(figsize=(12,8))

    plt.subplot(3,1,1)
    plt.plot(time_minutes, eda, lw=0.8)
    plt.title("Raw EDA")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Amplitude")

    plt.subplot(3,1,2)
    plt.plot(time_minutes, ecg, lw=0.8)
    plt.title("Raw ECG")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Amplitude")

    plt.subplot(3,1,3)
    plt.plot(time_minutes, trigger, lw=0.8)
    plt.title("Trigger Signal")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Amplitude")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
