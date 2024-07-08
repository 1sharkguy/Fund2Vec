import pandas as pd
import os

def combine_fund_data(file_paths):
    assets_dict = {}

    def update_assets_dict(df, fund_name):
        if 'Name' not in df.columns or 'Assets' not in df.columns:
            print(f"Error: Required columns 'Name' or 'Assets' not found in {fund_name}")
            return
        for _, row in df.iterrows():
            asset_name = row['Name']
            asset_value = row['Assets']
            if asset_name not in assets_dict:
                assets_dict[asset_name] = {}
            assets_dict[asset_name][fund_name] = asset_value

    for file_path in file_paths:
        fund_name = os.path.basename(file_path).split(' - ')[0]
        df = pd.read_csv(file_path)
        # print(f"Processing file: {file_path}")
        # print(f"Columns: {df.columns}")
        update_assets_dict(df, fund_name)
    
    combined_df = pd.DataFrame(assets_dict).T.fillna(0)
    combined_df.index.name = 'Asset Name'
    combined_df.columns.name = 'Fund Name'
    
    return combined_df.T

def save_combined_fund_data(file_paths, output_file):
    combined_df = combine_fund_data(file_paths)
    combined_df.to_csv(output_file)
    return output_file

def list_csv_files(directory='.'):
    csv_files = []
    
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv") and root == directory:
                # Create the relative path and add it to the list
                relative_path = os.path.relpath(os.path.join(root, file), start=directory)
                csv_files.append(relative_path)
    
    return csv_files

# Specify the directory to look for CSV files
directory = 'C:\\Users\\Divyansh Garg\\Desktop\\Fund2vec'  # Change this to your actual directory path

# List CSV files in the specified directory
sample_file_paths = list_csv_files(directory)
# print("CSV files found:", sample_file_paths)

# Output file path
output_file_path = 'combined_fund_data.csv'

# Save the combined data to a CSV file
output_file = save_combined_fund_data(sample_file_paths, output_file_path)

print(f"Combined data saved to: {output_file}")
