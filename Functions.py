# test

def hello():
	print('hello world')


# ~~~
# 1. function to collect 'all' data files from URL
# parameters:

## URL of the archive zip file
# archive_url = 'https://data.police.uk/data/archive/2021-12.zip'
# Directory to save extracted files
# output_directory = 'police_data_street'

## Date range for filtering subdirectories
# start_date = datetime(2020, 3, 1)
# end_date = datetime(2021, 3, 31)

import requests
import zipfile
import os
import io
from datetime import datetime

def download_and_filter_subdirectories(url, output_dir, start, end):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Downloading archive...")
    response = requests.get(url)
    
    # Ensure the download was successful
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            print("Extracting and filtering subdirectories...")
            for file_name in z.namelist():
                # Check if the file is within a subdirectory
                subdir_name = file_name.split('/')[0]  # Get the top-level directory name
                try:
                    # Parse the date from the subdirectory name (assuming format YYYY-MM)
                    subdir_date = datetime.strptime(subdir_name, '%Y-%m')
                    
                    if start <= subdir_date <= end:
                        print(f"Extracting: {file_name}")
                        z.extract(file_name, output_dir)
                except ValueError:
                    # Skip files or directories that don't match the expected date format
                    continue
    else:
        print(f"Failed to download archive. Status code: {response.status_code}")

# ~~~~~~
## 2. Retrieve files with 'street' in title (national)

def download_and_filter_street_files(url, output_dir, start, end):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Downloading archive...")
    response = requests.get(url)
    print(response.status_code)
    
    # Ensure the download was successful
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            print("Extracting files with '-street' in the title...")
            for file_name in z.namelist():
                # Check if the file is within a subdirectory and matches the date range
                subdir_name = file_name.split('/')[0]  # Get the top-level directory name
                try:
                    # Parse the date from the subdirectory name (assuming format YYYY-MM)
                    subdir_date = datetime.strptime(subdir_name, '%Y-%m')
                    
                    # Filter by date range and file name containing '-street'
                    if start <= subdir_date <= end and '-street' in file_name:
                        print(f"Extracting: {file_name}")
                        z.extract(file_name, output_dir)
                except ValueError:
                    # Skip files or directories that don't match the expected date format
                    continue
    else:
        print(f"Failed to download archive. Status code: {response.status_code}")

## Execute the function
#download_and_filter_street_files(archive_url, output_directory, start_date, end_date)

#print(f"Data with '-street' in the title has been extracted to: {output_directory}")


# ~~~~~~
## 3. How many records per month nationally?
import pandas as pd
def count_records_per_month(base_dir):
    records_per_month = []

    # Iterate through the subdirectories (each representing a month, e.g., '2020-03')
    for subdirectory in os.listdir(base_dir):
        subdirectory_path = os.path.join(base_dir, subdirectory)
        if os.path.isdir(subdirectory_path):  # Ensure it's a directory
            total_records = 0

            # Iterate through the CSV files in the subdirectory
            for file_name in os.listdir(subdirectory_path):
                if file_name.endswith('.csv'):  # Only process CSV files
                    file_path = os.path.join(subdirectory_path, file_name)
                    
                    try:
                        # Use pandas to read the CSV file and count the rows
                        data = pd.read_csv(file_path)
                        total_records += len(data)  # Add the number of rows to the total
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

            # Append the results for the current month
            records_per_month.append({'Month': subdirectory, 'Records': total_records})

    return records_per_month

## Get the record counts
#record_counts = count_records_per_month(base_directory)

## Convert the results to a DataFrame and save to CSV
#df = pd.DataFrame(record_counts)
#df.sort_values(by='Month', inplace=True)  # Sort by month
#df.to_csv(output_csv_file, index=False)

#print(f"Records per month have been saved to: {output_csv_file}")
# ~~~~~
## 4. Monthly sum for specific crime

#import os
#import pandas as pd

## Define the base directory where the downloaded data is stored
#base_directory = 'police_data'

## Output CSV file path
#output_csv_file = 'national_records_per_month(per_crime_types).csv'

def summarise_crime_types_per_month(base_dir):
    # List to hold the summary for each month
    summary_data = []

    # Iterate through the subdirectories (each representing a month, e.g., '2020-03')
    for subdirectory in os.listdir(base_dir):
        subdirectory_path = os.path.join(base_dir, subdirectory)
        if os.path.isdir(subdirectory_path):  # Ensure it's a directory
            # Dictionary to store crime type counts for the current month
            crime_type_counts = {}

            # Iterate through the CSV files in the subdirectory
            for file_name in os.listdir(subdirectory_path):
                if file_name.endswith('.csv'):  # Only process CSV files
                    file_path = os.path.join(subdirectory_path, file_name)
                    
                    try:
                        # Use pandas to read the CSV file
                        data = pd.read_csv(file_path)

                        # Ensure the 'Crime type' column exists
                        if 'Crime type' in data.columns:
                            # Count occurrences of each crime type in the file
                            crime_counts = data['Crime type'].value_counts().to_dict()

                            # Add the counts to the crime_type_counts dictionary
                            for crime_type, count in crime_counts.items():
                                crime_type_counts[crime_type] = crime_type_counts.get(crime_type, 0) + count
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

            # Add the month's data to the summary list
            summary_data.append({'Month': subdirectory, **crime_type_counts})

    # Convert the summary data to a DataFrame
    summary_df = pd.DataFrame(summary_data)

    # Fill missing values with 0 (for crime types not present in some months)
    summary_df.fillna(0, inplace=True)

    # Ensure all crime types are included as columns
    crime_types = [
        'Violence and sexual offences', 'Bicycle theft', 'Other theft',
        'Shoplifting', 'Anti-social behaviour', 'Burglary',
        'Criminal damage and arson', 'Drugs', 'Vehicle crime',
        'Public order', 'Possession of weapons', 'Robbery',
        'Other crime', 'Theft from the person'
    ]
    for crime_type in crime_types:
        if crime_type not in summary_df.columns:
            summary_df[crime_type] = 0

    return summary_df

## Get the crime summary
#crime_summary = summarise_crime_types_per_month(base_directory)

## Save the summary to a CSV file
#crime_summary.to_csv(output_csv_file, index=False)

#print(f"Crime summary per month has been saved to: {output_csv_file}")

# ~~~~~
## National / local comparison - Retrieving by county

#import os
#import pandas as pd

## Define the base directory where the downloaded data is stored
#base_directory = 'police_data'

## Define the county of interest
#target_county = 'Norfolk'

## Define the date range of interest
#start_date = '2020-03'
#end_date = '2021-03'

## Output CSV file path
#output_csv_file = 'crime_summary_norfolk.csv'

def aggregate_crimes_for_county_by_filename(base_dir, county, start, end):
    # List to hold the crime data for the target county across all months
    aggregated_data = []

    # Iterate through the subdirectories (each representing a month, e.g., '2020-03')
    for subdirectory in os.listdir(base_dir):
        # Ensure the subdirectory is within the date range
        if start <= subdirectory <= end:
            subdirectory_path = os.path.join(base_dir, subdirectory)

            if os.path.isdir(subdirectory_path):  # Ensure it's a directory
                total_crimes = 0

                # Iterate through the CSV files in the subdirectory
                for file_name in os.listdir(subdirectory_path):
                    # Check if the file name contains the county name
                    if county.lower() in file_name.lower() and file_name.endswith('.csv'):
                        file_path = os.path.join(subdirectory_path, file_name)
                        
                        try:
                            # Use pandas to read the CSV file
                            data = pd.read_csv(file_path)

                            # Count total rows (each row represents one crime)
                            total_crimes += len(data)
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")

                # Add the month's data to the aggregated list
                aggregated_data.append({'Month': subdirectory, 'Crimes': total_crimes})

    # Convert the aggregated data to a DataFrame
    aggregated_df = pd.DataFrame(aggregated_data)

    # Sort the data by month
    aggregated_df.sort_values(by='Month', inplace=True)

    return aggregated_df

## Get the crime summary for the county
#crime_summary = aggregate_crimes_for_county_by_filename(base_directory, target_county, start_date, end_date)

## Save the summary to a CSV file
#crime_summary.to_csv(output_csv_file, index=False)

#print(f"Crime summary for {target_county} has been saved to: {output_csv_file}")
# ~~~~~

#import os
#import pandas as pd

## Define the base directory where the downloaded data is stored
#base_directory = './police_data'

## Define the county of interest
#target_county = 'Norfolk'

## Output CSV file path
#output_csv_file = './crime_by_type_per_month_norfolk.csv'

def analyse_crime_by_type_per_month(base_dir, county):
    # List to hold the crime data for the target county across all months
    monthly_crime_data = []

    # Iterate through the subdirectories (each representing a month, e.g., '2020-03')
    for subdirectory in os.listdir(base_dir):
        subdirectory_path = os.path.join(base_dir, subdirectory)

        if os.path.isdir(subdirectory_path):  # Ensure it's a directory
            # Dictionary to store crime type counts for the current month
            crime_type_counts = {'Month': subdirectory}

            # Iterate through the CSV files in the subdirectory
            for file_name in os.listdir(subdirectory_path):
                # Check if the file name contains the county name
                if county.lower() in file_name.lower() and file_name.endswith('.csv'):
                    file_path = os.path.join(subdirectory_path, file_name)
                    
                    try:
                        # Use pandas to read the CSV file
                        data = pd.read_csv(file_path)

                        # Ensure the 'Crime type' column exists
                        if 'Crime type' in data.columns:
                            # Count occurrences of each crime type in the file
                            crime_counts = data['Crime type'].value_counts().to_dict()

                            # Update the monthly crime type counts
                            for crime_type, count in crime_counts.items():
                                crime_type_counts[crime_type] = crime_type_counts.get(crime_type, 0) + count
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

            # Add the month's data to the aggregated list
            monthly_crime_data.append(crime_type_counts)

    # Convert the aggregated data to a DataFrame
    crime_summary_df = pd.DataFrame(monthly_crime_data)

    # Fill missing values with 0 (for crime types not present in some months)
    crime_summary_df.fillna(0, inplace=True)

    return crime_summary_df

## Analysanalysee the crime data for the county by month and crime type
#crime_summary = analyse_crime_by_type_per_month(base_directory, target_county)

## Save the summary to a CSV file
#crime_summary.to_csv(output_csv_file, index=False)

#print(f"Crime summary by type per month for {target_county} has been saved to: {output_csv_file}")

# ~~~~~
## 6. Crime levels reported by County by Crime type

##import os
##import pandas as pd

## Define the base directory where the downloaded data is stored
#base_directory = './police_data'

## Define the county of interest
#target_county = 'Norfolk'

## Output CSV file path
#output_csv_file = './crime_summary_norfolk(by_crime_type).csv'

def analyse_crime_by_type_per_month(base_dir, county):
    # List to hold the crime data for the target county across all months
    monthly_crime_data = []

    # Iterate through the subdirectories (each representing a month, e.g., '2020-03')
    for subdirectory in os.listdir(base_dir):
        subdirectory_path = os.path.join(base_dir, subdirectory)

        if os.path.isdir(subdirectory_path):  # Ensure it's a directory
            # Dictionary to store crime type counts for the current month
            crime_type_counts = {'Month': subdirectory}

            # Iterate through the CSV files in the subdirectory
            for file_name in os.listdir(subdirectory_path):
                # Check if the file name contains the county name
                if county.lower() in file_name.lower() and file_name.endswith('.csv'):
                    file_path = os.path.join(subdirectory_path, file_name)
                    
                    try:
                        # Use pandas to read the CSV file
                        data = pd.read_csv(file_path)

                        # Ensure the 'Crime type' column exists
                        if 'Crime type' in data.columns:
                            # Count occurrences of each crime type in the file
                            crime_counts = data['Crime type'].value_counts().to_dict()

                            # Update the monthly crime type counts
                            for crime_type, count in crime_counts.items():
                                crime_type_counts[crime_type] = crime_type_counts.get(crime_type, 0) + count
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

            # Add the month's data to the aggregated list
            monthly_crime_data.append(crime_type_counts)

    # Convert the aggregated data to a DataFrame
    crime_summary_df = pd.DataFrame(monthly_crime_data)

    # Fill missing values with 0 (for crime types not present in some months)
    crime_summary_df.fillna(0, inplace=True)

    return crime_summary_df

## Analyse the crime data for the county by month and crime type
#crime_summary = analyse_crime_by_type_per_month(base_directory, target_county)

## Save the summary to a CSV file
#crime_summary.to_csv(output_csv_file, index=False)

#print(f"Crime summary by type per month for {target_county} has been saved to: {output_csv_file}")

# ~~~~~~~
## 7. 'Local' Relevance

#import os
#import pandas as pd

## Define the base directory where the downloaded data is stored
#base_directory = './police_data'

## Define the text to search for in the 'LSOA name' column
#search_text = 'Norwich'

## Output CSV file path
#output_csv_file = './crime_summary_norwich.csv'

def aggregate_crimes_by_lsoa(base_dir, search_text):
    # List to hold the aggregated data
    aggregated_data = []

    # Iterate through the subdirectories (each representing a month, e.g., '2020-01')
    for subdirectory in os.listdir(base_dir):
        subdirectory_path = os.path.join(base_dir, subdirectory)

        if os.path.isdir(subdirectory_path):  # Ensure it's a directory
            total_crimes = 0

            # Iterate through the CSV files in the subdirectory
            for file_name in os.listdir(subdirectory_path):
                if file_name.endswith('.csv'):  # Only process CSV files
                    file_path = os.path.join(subdirectory_path, file_name)

                    try:
                        # Use pandas to read the CSV file
                        data = pd.read_csv(file_path)

                        # Ensure the 'LSOA name' column exists
                        if 'LSOA name' in data.columns:
                            # Convert the 'LSOA name' column to strings explicitly
                            data['LSOA name'] = data['LSOA name'].astype(str)

                            # Filter rows where 'LSOA name' contains the search text
                            filtered_data = data[data['LSOA name'].str.contains(search_text, na=False)]

                            # Add the count of filtered rows to the total crimes
                            total_crimes += len(filtered_data)
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

            # Add the month's data to the aggregated list
            aggregated_data.append({'Month': subdirectory, 'Crimes': total_crimes})

    # Convert the aggregated data to a DataFrame
    aggregated_df = pd.DataFrame(aggregated_data)

    # Sort the data by month
    aggregated_df.sort_values(by='Month', inplace=True)

    return aggregated_df

## Get the crime summary for LSOA names containing the text "Norwich"
#crime_summary = aggregate_crimes_by_lsoa(base_directory, search_text)

## Save the summary to a CSV file
#crime_summary.to_csv(output_csv_file, index=False)

#print(f"Crime summary for LSOA names containing '{search_text}' has been saved to: {output_csv_file}")

# ~~~~~

## Summary Crimes by types per month Norwich

#import os
#import pandas as pd

## Define the base directory where the downloaded data is stored
#base_directory = './police_data'

## Define the text to search for in the 'LSOA name' column
#search_text = 'Norwich'

## Output CSV file path
#output_csv_file = './crime_summary_per_month_norwich(by_crime_type).csv'

def analyse_crime_by_type_per_month(base_dir, search_text):
    # List to hold the aggregated data
    monthly_crime_data = []

    # Iterate through the subdirectories (each representing a month, e.g., '2020-01')
    for subdirectory in os.listdir(base_dir):
        subdirectory_path = os.path.join(base_dir, subdirectory)

        if os.path.isdir(subdirectory_path):  # Ensure it's a directory
            # Dictionary to store crime type counts for the current month
            crime_type_counts = {'Month': subdirectory}

            # Iterate through the CSV files in the subdirectory
            for file_name in os.listdir(subdirectory_path):
                if file_name.endswith('.csv'):  # Only process CSV files
                    file_path = os.path.join(subdirectory_path, file_name)

                    try:
                        # Use pandas to read the CSV file
                        data = pd.read_csv(file_path)

                        # Ensure the 'LSOA name' and 'Crime type' columns exist
                        if 'LSOA name' in data.columns and 'Crime type' in data.columns:
                            # Convert the 'LSOA name' column to strings explicitly
                            data['LSOA name'] = data['LSOA name'].astype(str)

                            # Filter rows where 'LSOA name' contains the search text
                            filtered_data = data[data['LSOA name'].str.contains(search_text, na=False)]

                            # Group by 'Crime type' and count occurrences
                            crime_counts = filtered_data['Crime type'].value_counts().to_dict()

                            # Add crime counts to the monthly data
                            for crime_type, count in crime_counts.items():
                                crime_type_counts[crime_type] = crime_type_counts.get(crime_type, 0) + count
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

            # Append the month's crime type counts to the data
            monthly_crime_data.append(crime_type_counts)

    # Convert the aggregated data to a DataFrame
    crime_summary_df = pd.DataFrame(monthly_crime_data)

    # Fill missing values with 0 (for crime types not present in some months)
    crime_summary_df.fillna(0, inplace=True)

    return crime_summary_df

## Analyse the crime data for Norwich by month and crime type
#crime_summary = analyse_crime_by_type_per_month(base_directory, search_text)

## Save the summary to a CSV file
#crime_summary.to_csv(output_csv_file, index=False)

#print(f"Crime summary by type per month for LSOA names containing '{search_text}' has been saved to: {output_csv_file}")