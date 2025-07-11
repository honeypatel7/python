import pandas as pd 
import numpy as np 
from sklearn.cluster import KMeans 
import matplotlib.pyplot as plt 
 
# Step 1: Load the dataset 
df = pd.read_csv('C:\\Users\\lenovo\\Desktop\\python_lab\\online Retail.csv', encoding='ISO-8859-1') 

print(df.head()) 
print("\n") 
 
# Step 2: Data Cleaning 
# Drop rows with missing CustomerID 
df = df.dropna(subset=['CustomerID']) 
print(f"Number of rows after cleaning: {len(df)}") 
print("\n") 
 
# Calculate Total Amount Spent 
df['TotalAmountSpent'] = df['Quantity'] * df['UnitPrice'] 
 
# Group data by CustomerID 
customer_df = df.groupby('CustomerID').agg({ 
    'TotalAmountSpent': 'sum', 
    'Quantity': 'sum', 
    'InvoiceDate': 'max' 
}).reset_index() 
 
# Rename columns 
customer_df.rename(columns={'Quantity': 'TotalItemsPurchased', 'InvoiceDate': 'LastPurchaseDate'}, inplace=True) 
 
# Step 3: Data Preparation 
customer_df['AveragePurchaseValue'] = customer_df['TotalAmountSpent'] / customer_df['TotalItemsPurchased'] 
 
# Step 4: Descriptive Statistics 
print(customer_df[['TotalAmountSpent', 'TotalItemsPurchased']].describe()) 
 
# Step 5: Check if there are enough customers for clustering and adjust n_clusters 
n_customers = len(customer_df) 
print(f"Number of customers after aggregation: {n_customers}") 
 
# If there are fewer than 3 customers, reduce the number of clusters accordingly 
n_clusters = min(3, n_customers)  # Set to 3 if there are enough customers, otherwise use all available customers 
 
if n_customers >= 2: 
    print(f"Performing KMeans clustering with {n_clusters} clusters.") 

 
    # Step 6: Customer Segmentation using K-means 
    kmeans = KMeans(n_clusters=n_clusters, random_state=42) 
    customer_df['Segment'] = kmeans.fit_predict(customer_df[['TotalAmountSpent', 'TotalItemsPurchased']]) 
else: 
    print("Not enough data to perform clustering. Setting default segment.") 
    # Create a default segment if not enough data for clustering 
    customer_df['Segment'] = 0  # All customers are assigned to the same segment 
 
# Step 7: Visualization 
plt.scatter(customer_df['TotalAmountSpent'], customer_df['TotalItemsPurchased'], 
            c=customer_df['Segment']) 
plt.xlabel('Total Amount Spent') 
plt.ylabel('Total Items Purchased') 
plt.title('Customer Segmentation') 
plt.show() 
 
# Step 8: Customer Insights 
segment_insights = customer_df.groupby('Segment').mean() 
print("\nCustomer Segment Insights:") 
print(segment_insights) 
 
# Step 9: Customer Engagement Recommendations 
 
def recommend_engagement(segment): 
    if segment == 0:  # Adjust based on your specific cluster analysis 
        return "High Spenders: Offer loyalty rewards, exclusive discounts, and premium product recommendations." 
    elif segment == 1: 
        return "Frequent Shoppers: Provide personalized product suggestions and regular updates on new arrivals." 
    elif segment == 2: 
        return "Inactive Customers: Send re-engagement emails with special offers or discounts to bring them back." 
    else: 
        return "General: Maintain regular engagement with newsletters and product updates." 
 
# Apply recommendations to each customer 
customer_df['Recommendation'] = customer_df['Segment'].apply(recommend_engagement) 
 
# Display the first few rows to see the recommendations 
print("\nCustomer Recommendations:") 
print(customer_df[['CustomerID', 'Segment', 'Recommendation']].head())