import pandas as pd
from IPython.display import display
import os
from colorama import Fore, Style, init
init()


def check_nrslips_total(df):
    """Check that NrSlips equals the sum of other slip columns."""
    nrslips_col = next((col for col in df.columns if col.lower() == 'nrslips'), None)
    other_slip_cols = [col for col in df.columns if 'slip' in col.lower() and col.lower() != 'nrslips']
    
    if nrslips_col is None or not other_slip_cols:
        print(f"Warning: Could not find NrSlips or other slip columns")
        return False
    
    other_sum = df[other_slip_cols].sum(axis=1)
    matches = (df[nrslips_col] == other_sum).all()
    mismatches = (df[nrslips_col] != other_sum).sum()
    
    print(f"NrSlips matches sum of other slip columns: {matches}")
    if mismatches > 0:
        print(f"Mismatches found in {mismatches} row(s)")
    return matches

def check_totaldropped_equals_slips(df):
    """Check that TotalDropped equals the sum of all slip columns including NrSlips."""
    total_dropped_col = next((col for col in df.columns if col.lower() == 'totaldropped'), None)
    slip_cols = [col for col in df.columns if 'slip' in col.lower()]

    if total_dropped_col is None or not slip_cols:
        print(f"Warning: Could not find TotalDropped or slip columns")
        return False
    
    total_slips = df[slip_cols].sum().sum()
    matches = (df[total_dropped_col].iloc[-1] == total_slips)
    print(f"Total dropped column final number equals all slips: {matches}")

    return matches

def check_velocity_comparison(df):
    """Check that non-slip trials have faster velocity than slip trials."""
    velocity_col = next((col for col in df.columns if 'velocity' in col.lower()), None)
    trial_type_col = next((col for col in df.columns if col.lower() == 'trialtype'), None)
    if trial_type_col is None:
        trial_type_col = next((col for col in df.columns if 'trialtype' in col.lower() or 'blocktype' in col.lower()), None)
    
    if velocity_col is None or trial_type_col is None:
        print(f"Warning: Could not find velocity or trial type column")
        return False
    
    trial_type_str = df[trial_type_col].astype(str)
    slip_trials = df[trial_type_str == 'SlipTrial']
    non_slip_trials = df[trial_type_str == 'NonSlipTrial']
    
    slip_avg_velocity = slip_trials[velocity_col].mean()
    non_slip_avg_velocity = non_slip_trials[velocity_col].mean()
    
    result = non_slip_avg_velocity > slip_avg_velocity
    print(f"Slip trials avg velocity: {slip_avg_velocity:.2f}, Non-slip trials avg velocity: {non_slip_avg_velocity:.2f}")
    print(f"Non-slip trials are faster: {result}")
    return result

def check_stress_block_velocity(df):
    """Compare velocity between StressBlock and NonStressBlock."""
    velocity_col = next((col for col in df.columns if 'velocity' in col.lower()), None)
    block_type_col = next((col for col in df.columns if col.lower() == 'blocktype'), None)
    
    if velocity_col is None or block_type_col is None:
        print(f"Warning: Could not find velocity or block type column")
        return False
    
    block_type_str = df[block_type_col].astype(str)
    stress_blocks = df[block_type_str == 'StressBlock']
    non_stress_blocks = df[block_type_str == 'NonStressBlock']
    
    stress_avg_velocity = stress_blocks[velocity_col].mean()
    non_stress_avg_velocity = non_stress_blocks[velocity_col].mean()
    
    print(f"StressBlock avg velocity: {stress_avg_velocity:.2f}, NonStressBlock avg velocity: {non_stress_avg_velocity:.2f}")
    return True

def check_stress_block_balance(df):
    """Check that NonStressBlocks and StressBlocks are equal when Training is FALSE."""
    training_col = next((col for col in df.columns if col.lower() == 'training'), None)
    block_type_col = next((col for col in df.columns if col.lower() == 'blocktype'), None)
    
    if training_col is None or block_type_col is None:
        print(f"Warning: Could not find Training or BlockType column")
        return False
    
    # Filter for Training == FALSE
    non_training = df[df[training_col] == False]
    
    block_type_str = non_training[block_type_col].astype(str)
    non_stress_count = non_training[block_type_str == 'NonStressBlock'].shape[0]
    stress_count = non_training[block_type_str == 'StressBlock'].shape[0]
    
    result = stress_count == non_stress_count
    print(f"NonTraining: StressBlock count: {stress_count}, NonStressBlock count: {non_stress_count}")
    print(f"Equal counts: {result}")
    return result

def check_slip_trial_slips(df):
    """Check that Slip Trials have more total slips than non-slip trials."""
    # Find all slip count columns (NrErrorSlips, NrSlips, NrOtherSlips, etc.)
    slip_cols = [col for col in df.columns if 'slip' in col.lower()]
    
    # Find trial type column
    trial_type_col = next((col for col in df.columns if col.lower() == 'trialtype'), None)
    if trial_type_col is None:
        trial_type_col = next((col for col in df.columns if 'trialtype' in col.lower() or 'blocktype' in col.lower()), None)
    
    if not slip_cols or trial_type_col is None:
        print(f"Warning: Could not find required columns. Slip columns: {slip_cols}, Trial type: {trial_type_col}")
        return False
    
    # Identify slip vs non-slip trials
    trial_type_str = df[trial_type_col].astype(str)
    slip_trials = df[trial_type_str == 'SlipTrial']
    non_slip_trials = df[trial_type_str == 'NonSlipTrial']
    
    # Sum all slip columns for each trial type
    slip_total = slip_trials[slip_cols].sum().sum()
    non_slip_total = non_slip_trials[slip_cols].sum().sum()
    
    result = slip_total > non_slip_total
    print(f"Slips in Slip trials total: {slip_total}, Slips in Non-slip trials total: {non_slip_total}")
    print(f"Slip trials have more slips: {result}")
    return result

def check_trial_duration(df):
    """Calculate average trial duration and total duration in minutes."""
    time_col = next((col for col in df.columns if col.lower() == 'time'), None)
    
    if time_col is None:
        print(f"Warning: Could not find Time column")
        return False
    
    # Calculate trial durations (difference between consecutive times)
    trial_durations = df[time_col].diff().dropna()
    avg_trial_duration_sec = trial_durations.mean()
    avg_trial_duration_min = avg_trial_duration_sec / 60
    
    # Total duration is the maximum time value
    total_duration_sec = df[time_col].max()
    total_duration_min = total_duration_sec / 60
    
    print(f"Average trial duration: {avg_trial_duration_min:.2f} minutes ({avg_trial_duration_sec:.2f} seconds)")
    print(f"Total duration: {total_duration_min:.2f} minutes ({total_duration_sec:.2f} seconds)")
    is_close = abs(total_duration_sec - 959) < 2  # Allowing minor rounding error
    print(f"Total duration is close to 959 seconds: {is_close}")
    return is_close

def check_stress_dropped(df):
    """Check if more items dropped during stress vs non-stress periods."""
    total_dropped_col = next((col for col in df.columns if col.lower() == 'totaldropped'), None)
    block_type_col = next((col for col in df.columns if col.lower() == 'blocktype'), None)
    
    if total_dropped_col is None or block_type_col is None:
        print(f"Warning: Could not find TotalDropped or BlockType column")
        return False
    
    block_type_str = df[block_type_col].astype(str)
    stress_dropped = df[block_type_str == 'StressBlock'][total_dropped_col].sum()
    non_stress_dropped = df[block_type_str == 'NonStressBlock'][total_dropped_col].sum()
    
    result = stress_dropped > non_stress_dropped
    print(f"StressBlock total dropped: {stress_dropped}, NonStressBlock total dropped: {non_stress_dropped}")
    print(f"Stress has more dropped: {result}")
    return result

def main(FILE_PATH = r"C:\Users\stefan\Documents\Unreal Projects\UnrealPythonTools\CraneGame\logs\20251181420_TEST_CraneOut.xlsx"): 
    # If FILE_PATH is a relative path, convert it to absolute
    
    if not os.path.isabs(FILE_PATH):
        FILE_PATH = os.path.abspath(FILE_PATH)
    
    if not os.path.exists(FILE_PATH):
        print(f"Error: File not found: {FILE_PATH}")
        return
    
    # Load CSV or Excel based on file extension
    if FILE_PATH.lower().endswith('.csv'):
        df = pd.read_csv(FILE_PATH)
    else:
        df = pd.read_excel(FILE_PATH)
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('[^a-zA-Z0-9_]', '', regex=True)
    
    print(f"Checking logfile {os.path.basename(FILE_PATH)}...")

    divider = "-" * 50
    print((Fore.GREEN + "OK" if check_nrslips_total(df) else Fore.RED + "ERROR") + Style.RESET_ALL)
    print(divider)
    print((Fore.GREEN + "OK" if check_totaldropped_equals_slips(df) else Fore.RED + "ERROR") + Style.RESET_ALL)
    print(divider)
    print((Fore.GREEN + "OK" if check_stress_dropped(df) else Fore.RED + "ERROR") + Style.RESET_ALL)
    print(divider)
    print((Fore.GREEN + "OK" if check_velocity_comparison(df) else Fore.RED + "ERROR") + Style.RESET_ALL)
    print(divider)
    print((Fore.GREEN + "OK" if check_stress_block_velocity(df) else Fore.RED + "UNSURE") + Style.RESET_ALL)
    print(divider)
    print((Fore.GREEN + "OK" if check_stress_block_balance(df) else Fore.RED + "ERROR") + Style.RESET_ALL)
    print(divider)
    print((Fore.GREEN + "OK" if check_slip_trial_slips(df) else Fore.RED + "ERROR") + Style.RESET_ALL)
    print(divider)
    print((Fore.GREEN + "OK" if check_trial_duration(df) else Fore.RED + "ERROR") + Style.RESET_ALL)
    print(divider)

if __name__ == "__main__":
    main()
