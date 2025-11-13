import scipy.io as sio
import sys
import os
from IPython.display import display
import numpy as np
import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt



def clean_labels(labels_in):

    return [label.strip() for label in labels_in.flatten()]

def main(biopack_data_fn = r"C:\Users\stefan\Documents\Unreal Projects\UnrealPythonTools\CraneGame\example_data\TEST N.mat"):

    if os.path.exists(biopack_data_fn):
        print(f"Found file: {biopack_data_fn}")

        mat_data = sio.loadmat(biopack_data_fn)

        #print(mat_data)
        #print(f"Type: {type(mat_data)}")

        all_data = mat_data['data']
        all_labels = clean_labels(mat_data['labels'])
        all_isi = mat_data['isi']

        print(f"All ISI: {all_isi[0][0]}")

        all_units = mat_data['units']

    # Get EDA data

    print(all_labels)
    eda_idx = None
    eda_idx = [i for i,s in enumerate(all_labels) if "EDA" in s]

    if eda_idx is None:
        print("Cannot find EDA data")
    else: 
        print(f"EDA idx: {eda_idx}")

    eda_data = all_data[:,eda_idx].squeeze()

    print(eda_data)

    eda_units = all_units[eda_idx]
    eda_isi = all_isi.squeeze()/1000 # As in ms

    print(f"EDA: Found {len(eda_data)} pts. Mean is: {eda_data.mean()} ISI: {eda_isi} seconds UNITS: {eda_units[0]} ")

    eda_sf = 1/eda_isi # Hz should be in seconds :)

    eda_time_stamps = np.arange(len(eda_data))/eda_sf

    eda_df = pd.DataFrame({"TimeStamp": eda_time_stamps, "Value": eda_data})

    #display(eda_df)

    # Split preprocessing and analysis for method control
    eda_raw = eda_df['Value'].values
    eda_cleaned = nk.eda_clean(eda_raw, sampling_rate=eda_sf,method="biosppy")
    eda_decomposed = nk.eda_phasic(eda_cleaned, sampling_rate=eda_sf)
    
    eda_peak_methods = ['neurokit', 'gamboa2008', 'kim2004', 'vanhalem2020', 'nabian2018']
    peak_times_dict = {}

    eda_total_time = eda_df["TimeStamp"].iloc[-1]/60
    print(f"Total length of sampling period: {eda_total_time} minutes")
    
    print("-" * 50)
    
    for m in eda_peak_methods:
        try:
            eda_peaks_info = nk.eda_peaks(eda_decomposed["EDA_Phasic"], sampling_rate=eda_sf, method=m)
            scr_peak_times = eda_peaks_info[1]['SCR_Peaks']
            peak_times_dict[m] = len(scr_peak_times)
            print(f"Method: {m}, N peaks per min: {len(scr_peak_times)/eda_total_time}")
        except Exception as e:
            print(f"Method: {m} failed with error: {e}")
            peak_times_dict[m] = None
    
    print("-" * 10)

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        main(biopack_data_fn = sys.argv[1])
    else:
        main()