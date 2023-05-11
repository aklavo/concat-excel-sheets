import pandas as pd
import glob

# Get path to data folder from user
folder_path = str(input("Enter data folder path:"))
output_file_name = str(input("Enter output file name:"))

# List all CSV files in the directory
csv_files = glob.glob(f"{folder_path}\*.csv")

# Read each CSV file into a Pandas DataFrame and append to a list
# Remove any duplicate datetime rows and any instances of non 5 min interval datetimes
dfs = []
for file in csv_files:
    df = pd.read_csv(file, header=0, usecols=[0, 1], parse_dates=[0])
    df = (
        df.drop_duplicates("Time", ignore_index=True)
        .set_index("Time")
        .asfreq("5min")
        .dropna()
    )
    dfs.append(df)

# Concatenate all DataFrames into a single DataFrame
df_merged = pd.concat(dfs, axis=1, join="outer").reset_index()

# Save the merged DataFrame to a CSV file
df_merged.to_csv(f"{folder_path}\{output_file_name}", index=False)
