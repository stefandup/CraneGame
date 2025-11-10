import pandas as pd
from IPython.display import display
from colorama import Fore, Style, init

# Initialize colorama for Windows terminal support
init(autoreset=True)

# Load and display the CSV file
#SAVED_DIR = r"C:\Users\stefan\Documents\Unreal Projects\TowerCranePackagedBetaTrig\Windows\TowerCrane\Saved"
SAVED_DIR=r"C:\Users\stefan\Documents\Unreal Projects\UnrealPythonTools\CraneGame\logs"
#TARGET_LOG = "2025154_TEST_CraneOut.csv"
TARGET_LOG=r"20251181420_TEST_CraneOut.xlsx"

#df = pd.read_csv(f"{SAVED_DIR}\\{TARGET_LOG}")
df = pd.read_excel(f"{SAVED_DIR}\\{TARGET_LOG}")


# Check for empty values
empty_count = df.isnull().sum().sum()
if empty_count > 0:
    print(f"{Fore.YELLOW}WARNING: Found {empty_count} empty value(s) in the data:{Style.RESET_ALL}")

else:
    print("No empty values found in the data.")

display(df)

# Calculate total time in minutes
total_time_seconds = df['Time'].max()
total_time_minutes = total_time_seconds / 60

print(f"Total time: {total_time_minutes:.2f} minutes ({total_time_seconds:.2f} seconds)")

# Compute inter-trial length (time difference between consecutive rows)
inter_trial_lengths = df['Time'].diff()

print(f"\nInter-trial lengths (time differences between consecutive rows):")
print(f"  Count: {len(inter_trial_lengths.dropna())} intervals")
print(f"  Mean: {inter_trial_lengths.mean():.4f} seconds ({inter_trial_lengths.mean() / 60:.4f} minutes)")
print(f"  Min: {inter_trial_lengths.min():.4f} seconds")
print(f"  Max: {inter_trial_lengths.max():.4f} seconds ({inter_trial_lengths.max() / 60:.4f} minutes)")


