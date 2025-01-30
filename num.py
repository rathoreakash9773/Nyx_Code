import pandas as pd
import numpy as np

# Define the file path
file_path ="/home/dev2/.conda/envs/Ankit/Mastercsvs/Photographers_Master.csv"

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Define the column name
column_name = 'Followers'

# Define a function to convert strings with 'K' or 'M' suffixes to numeric values
def convert_to_numeric(value):
    if pd.isna(value):  # Check for NaN values
        return np.nan
    value_str = str(value)  # Convert the value to a string first
    if 'K' in value_str:
        return int(float(value_str.replace('K', '')) * 1000)
    elif 'M' in value_str:
        return int(float(value_str.replace('M', '')) * 1000000)
    else:
        return int(value_str)

# Apply the function to the specified column
df[column_name] = df[column_name].apply(convert_to_numeric)

# Define the path for the modified file
modified_file_path = '/home/dev2/.conda/envs/Ankit/Mastercsvs/Photographers_Master_updated.csv'

# Save the modified DataFrame back to CSV
df.to_csv(modified_file_path, index=False)
