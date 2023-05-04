import os
import pandas as pd

folder_path = r'C:\Users\andrewkl\McKinstry\MTN Projects - 12 Trends\Scott Bio BAS Trends 4.13'

# Get a list of all the .csv files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Read in each .csv file store it as a dataframe, then store it in a list
dfs = []
for file in csv_files:
    if file == csv_files[0]:
        df = pd.read_csv(os.path.join(folder_path, file), usecols=[0, 1])
    else:
        df = pd.read_csv(os.path.join(folder_path, file), usecols=[1])

    dfs.append(df)


# Merge all the dataframes into a single dataframe based on the Time column, NaN unavalible data
merged_df = pd.concat(dfs, axis=1)

# Export the merged dataframe as a single .csv file
merged_df.to_csv(os.path.join(folder_path, 'output.csv'), index=False)
