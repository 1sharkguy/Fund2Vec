import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import csv

def generate_mutual_fund_csv(soup, file_name):
    # Finding the table with class 'tb10Table holdings101Table'
    table = soup.find('table', class_='tb10Table holdings101Table')
    if not table:
        print(f"Table not found in {file_name}.")
        return

    data = []
    # Finding the header row
    headers = table.find('thead').find('tr')
    cols = headers.find_all('th')
    if len(cols) >= 4:
        name_header = cols[0].get_text().strip()
        assets_header = cols[3].get_text().strip()
        data.append([name_header, assets_header])

    # Finding all the data rows
    rows = table.find('tbody').find_all('tr', class_='holdings101Row')

    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 4:
            name = cols[0].get_text().strip()
            assets = cols[3].get_text().strip().replace('%', '').strip()
            assets = float(assets) / 100  # Convert percentage to decimal
            data.append([name, assets])
    
    # Writing the data to a CSV file
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"CSV file '{file_name}' generated successfully.")

# List of file paths to process
def list_html_files(folder_path):
    html_files = []
    
    # Walk through the directory
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".html"):
                # Create the relative path and add it to the list
                relative_path = os.path.relpath(os.path.join(root, file), folder_path)
                html_files.append(relative_path)
    
    return html_files

# Example usage
folder_path = 'Files'  # Replace with the path to your folder
files = list_html_files(folder_path)
print(files)
for file_path in files:
    full_path = os.path.join(folder_path, file_path)
    with open(full_path, 'r') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'lxml')
        # Extract the mutual fund name from the file name to create the CSV file name
        fund_name = os.path.splitext(os.path.basename(file_path))[0]
        csv_file_name = f"{fund_name}.csv"
        generate_mutual_fund_csv(soup, csv_file_name)
