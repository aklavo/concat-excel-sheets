import os
import pandas as pd
import sys

# Get path to data folder from user
folder_path = str(input("Enter data folder path:"))

# Get a list of all the .csv files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Read in each .csv file store it as a dataframe, then store it in a list
dfs = []
for i, file in enumerate(csv_files):
    df = pd.read_csv(os.path.join(folder_path, file), header=0, index_col=False, usecols=[0, 1], parse_dates=[0])
    start_time = df['Time'].iloc[0]
    end_time = df['Time'].iloc[-1]
    dfs.append({'df': df, 'start_time': start_time, 'end_time': end_time})

# Determine the maximum start and end times
start_times = [d['start_time'] for d in dfs]
end_times = [d['end_time'] for d in dfs]
max_start_time = max(start_times)
max_end_time = max(end_times)

# Create a DataFrame with a datetime range using max/min times
dt_range = pd.date_range(start=max_start_time, end=max_end_time, freq='5T')

# Convert the datetime range to a DataFrame
merged_df = pd.DataFrame({'Time': dt_range})

# Merge all the dataframes into a single dataframe based on the Time column, NaN unavalible data
for d in dfs:
    merged_df = merged_df.merge(d["df"], how='left', on='Time')

# Export the merged dataframe as a single .csv file
merged_df.to_csv(os.path.join(folder_path, 'Scoot-BIO-BAS-Combined.csv'), index=False)
