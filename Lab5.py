

import os
import json

# Step 1: Load all JSON files from a directory and subdirectories
def load_covid_data(data_directory):
    covid_data = []
    for root, dirs, files in os.walk(data_directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    covid_data.append(data)
    return covid_data

# Step 2: Calculate summary statistics for each country
def calculate_statistics(covid_data):
    country_stats = {}
    
    for data in covid_data:
        country = data['country']
        if country not in country_stats:
            country_stats[country] = {
                'total_confirmed': 0,
                'total_deaths': 0,
                'total_recovered': 0
            }
        
        country_stats[country]['total_confirmed'] += data['confirmed_cases']['total']
        country_stats[country]['total_deaths'] += data['deaths']['total']
        country_stats[country]['total_recovered'] += data['recovered']['total']
    
    # Calculate total active cases for each country
    for country, stats in country_stats.items():
        stats['total_active'] = stats['total_confirmed'] - stats['total_deaths'] - stats['total_recovered']
    
    return country_stats

# Step 3: Determine the top 5 countries with highest and lowest confirmed cases
def get_top_countries(country_stats):
    sorted_countries = sorted(country_stats.items(), key=lambda x: x[1]['total_confirmed'], reverse=True)
    
    top_5_highest = sorted_countries[:5]
    top_5_lowest = sorted_countries[-5:]
    
    return top_5_highest, top_5_lowest

# Step 4: Generate the summary report and save it to a JSON file
def generate_summary_report(country_stats, top_5_highest, top_5_lowest, output_filename="covid19_summary.json"):
    summary = {
        "COVID-19 Statistics by Country": [
            f"{country}: Confirmed: {stats['total_confirmed']}, Deaths: {stats['total_deaths']}, Recovered: {stats['total_recovered']}, Active: {stats['total_active']}"
            for country, stats in country_stats.items()
        ],
        "Top 5 Countries with Highest Confirmed Cases": [
            f"{country}: {stats['total_confirmed']}" for country, stats in top_5_highest
        ],
        "Top 5 Countries with Lowest Confirmed Cases": [
            f"{country}: {stats['total_confirmed']}" for country, stats in top_5_lowest
        ]
    }
    
    with open(output_filename, 'w') as f:
        json.dump(summary, f, indent=4)

# Step 5: Print top 5 countries with highest and lowest confirmed cases
def print_top_countries(top_5_highest, top_5_lowest):
    print("\nTop 5 Countries with Highest Confirmed Cases:")
    for country, stats in top_5_highest:
        print(f"{country}: {stats['total_confirmed']}")

    print("\nTop 5 Countries with Lowest Confirmed Cases:")
    for country, stats in top_5_lowest:
        print(f"{country}: {stats['total_confirmed']}")

# Step 6: Main function to run the entire process
def main(data_directory):
    try:
        covid_data = load_covid_data(data_directory)
        country_stats = calculate_statistics(covid_data)
        top_5_highest, top_5_lowest = get_top_countries(country_stats)
        
        # Generate summary file
        generate_summary_report(country_stats, top_5_highest, top_5_lowest)
        
        # Print top 5 countries with highest and lowest confirmed cases
        print_top_countries(top_5_highest, top_5_lowest)
        
        print("\nSummary file 'covid19_summary.json' has been generated successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Set the data directory to the path where the JSON files are located
data_directory = "C:\\Users\\Honey\\Desktop\\python_lab\\covid_data"

# Run the main function
main(data_directory)


