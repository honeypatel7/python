import os 
import pandas as pd 
 

print("Current working directory:", os.getcwd()) 
print("Directory contents:", os.listdir()) 
 
# Function to read all sales data from CSV files in a directory and its subdirectories 
def read_sales_data(directory): 
    all_data = [] 
    for root, _, files in os.walk(directory): 
        for file in files: 
            if file.endswith('.csv'): 
                file_path = os.path.join(root, file) 
                data = pd.read_csv(file_path) 
                all_data.append(data) 
    return pd.concat(all_data, ignore_index=True) 
 
# Function to calculate total and average sales per product 
def calculate_sales_summary(sales_data, product_names): 
    try: 
        # Group by Product ID and calculate total quantity sold 
        total_sales = sales_data.groupby('Product ID')['Quantity sold'].sum().reset_index() 
         
        # Merge with product names 
        summary = pd.merge(total_sales, product_names, on='Product ID', how='left') 
         
        # Convert 'Date' column to datetime format if it exists 
        if 'Date' in sales_data.columns: 
            sales_data['Date'] = pd.to_datetime(sales_data['Date']) 
            # Calculate the average quantity sold per month 
            total_months = sales_data['Date'].dt.to_period('M').nunique()  # Unique months 
            summary['Average Quantity Sold per Month'] = summary['Quantity sold'] / total_months 
        else: 
            summary['Average Quantity Sold per Month'] = summary['Quantity sold']  
         
        return summary 
    except Exception as e: 
        print(f"Error in calculating sales summary: {e}") 
        return pd.DataFrame()  # Return an empty DataFrame on error 

 
 
# Function to determine the top 5 best-selling products 
def get_top_selling_products(sales_summary): 
    return sales_summary.sort_values(by='Quantity sold', ascending=False).head(5) 
 
# Main function to execute the operations 
def main(): 
    try: 
        # Set the directories to '2011' and '2012' within 'prac4' 
        base_directory = os.getcwd() 
        directories = [os.path.join(base_directory, '2023'), os.path.join(base_directory, '2022')] 
 
        # Debugging lines to check paths 
        print("Current working directory:", base_directory) 
        for directory in directories: 
            print(f"Checking directory {directory}") 
            print("Files in the directory:", os.listdir(directory)) 
 
        # Read the product names file 
        product_names = pd.read_csv('products.csv') 
         
        # Read sales data from both directories 
        all_sales_data = [] 
        for directory in directories: 
            sales_data = read_sales_data(directory) 
            all_sales_data.append(sales_data) 
         
        # Combine sales data from both folders 
        combined_sales_data = pd.concat(all_sales_data, ignore_index=True) 
         
        # Calculate the sales summary 
        sales_summary = calculate_sales_summary(combined_sales_data, product_names) 
         
        # Get the top 5 best-selling products 
        top_selling_products = get_top_selling_products(sales_summary) 
         
        # Save the sales summary to a CSV file 
        top_selling_products.to_csv('sales_summary.csv', index=False) 
         
        # Print the top 5 best-selling products 
        print("\nTop 5 Best-Selling Products:") 
        print(top_selling_products[['Product ID', 'Product Name', 'Quantity sold', 'Average Quantity Sold per Month']].to_string(index=False)) 
 
        print("\nSales summary has been saved to 'sales_summary.csv'.") 
        print("Name: Honey Patel") 
        print("Roll number: 22BCP402") 
 
    except Exception as e: 
        print(f"An error occurred: {e}") 
 
if __name__ == "__main__": 
    main()