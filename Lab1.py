import os

# Function to read all reviews from a file
def read_all_reviews(file_path):
    reviews = []
    invalid_reviews = 0

    with open(file_path, 'r') as f:
        for line in f:
            parts = line.split(' ', 4)
            if len(parts) == 5:
                custID = parts[0]
                prodID = parts[1]
                revdate = parts[2]
                revrate = parts[3]
                revtext = parts[4]
                try:
                    revrate = int(revrate)
                    reviews.append((custID, prodID, revdate, revrate, revtext))
                except ValueError:
                    invalid_reviews += 1
            else:
                invalid_reviews += 1

    return reviews, invalid_reviews

# Function to calculate average ratings
def calculate_average_ratings(reviews):
    product_ratings = {}

    for review in reviews:
        prodID = review[1]
        revrate = review[3]

        if prodID not in product_ratings:
            product_ratings[prodID] = []
        product_ratings[prodID].append(revrate)

    average_ratings = {prodID: sum(ratings) / len(ratings) for prodID, ratings in product_ratings.items()}

    return average_ratings

# Function to write results to a file
def write_results(filename, total_reviews, total_valid, total_invalid, top_products):
    with open(filename, 'w') as f:
        f.write('Summary Report\n')
        f.write('Total reviews: ' + str(total_reviews) + '\n')
        f.write('Total valid reviews: ' + str(total_valid) + '\n')
        f.write('Total invalid reviews: ' + str(total_invalid) + '\n')
        f.write('Top 3 products:\n')
        for prod in top_products:
            f.write('Product ID: ' + prod[0] + ' Average rating: ' + str(prod[1]) + '\n')

# Main function
def main():
    review_directory = 'review_files'  # Directory containing the review files
    review_files = [os.path.join(review_directory, file) for file in os.listdir(review_directory)]

    all_reviews = []
    total_invalid_reviews = 0

    for file in review_files:
        reviews, invalid_reviews = read_all_reviews(file)
        all_reviews.extend(reviews)
        total_invalid_reviews += invalid_reviews

    total_reviews = len(all_reviews)
    average_ratings = calculate_average_ratings(all_reviews)
    sorted_avg_ratings = sorted(average_ratings.items(), key=lambda x: x[1], reverse=True)

    top_products = sorted_avg_ratings[:3]

    # Writing results to summary.txt
    write_results('summary.txt', total_reviews, total_reviews - total_invalid_reviews, total_invalid_reviews, top_products)
    
    # Print confirmation message
    print("summary.txt file has been generated successfully!")

if __name__ == "__main__":
    main()
