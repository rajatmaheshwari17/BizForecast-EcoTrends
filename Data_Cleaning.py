import os
import pandas as pd
import numpy as np

input_directory = "."
excel_files = [file for file in os.listdir(input_directory) if file.endswith(".xlsx")]
combined_data = pd.DataFrame()

def clean_data(input_file):
    data = pd.read_excel(input_file, header=7)
    data['Date'] = pd.to_datetime(data['Date']).dt.date
    data.replace(["", " ", None], np.nan, inplace=True)

    data.columns = [
        'Date', 
        'Company Name', 
        'Vch Type', 
        'Vch Number', 
        'Inwards Quantity', 
        'Inwards Value', 
        'Outwards Quantity', 
        'Outwards Value', 
        'Closing Quantity', 
        'Closing Value'
    ]

    return data

for excel_file in excel_files:
    cleaned_data = clean_data(os.path.join(input_directory, excel_file))
    combined_data = pd.concat([combined_data, cleaned_data])

combined_data.to_csv('combined_cleaned_data.csv', index=False)

print("Data cleaning and combination completed.")
