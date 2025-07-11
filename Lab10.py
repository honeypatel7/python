import os
import logging

# Set up logging configuration
logging.basicConfig(filename='grades_processing.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Read the data from text files in the directory
def read_grades_from_directory(directory):
    grades = []

    # Check if the directory exists
    if not os.path.exists(directory):
        logging.error(f"Directory '{directory}' does not exist.")
        return grades

    # Read files from the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)  # Create the full path to the file
        logging.info(f"Processing file: {file_path}")
        
        try:
            with open(file_path, 'r') as file:  # Open each file
                for line in file:
                    # Assuming each line has: Name, Maths, Science, English (space separated)
                    parts = line.strip().split()
                    if len(parts) == 4:
                        grades.append({
                            'Name': parts[0],  # Student's name
                            'Maths': float(parts[1]),  # Maths score
                            'Science': float(parts[2]),  # Science score
                            'English': float(parts[3])   # English score
                        })
                    else:
                        logging.warning(f"Invalid line format in file {file_path}: {line}")
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {e}")
    
    return grades

# Step 3: Calculate the average for each student
def calculate_average(grades):
    logging.info("Calculating averages for each student.")
    for student in grades:
        student['Average'] = (student['Maths'] + student['Science'] + student['English']) / 3  # Calculate average

# Step 4: Store the student's name and their corresponding average score in a new list
def create_average_dict(grades):
    average_dict = []
    for student in grades:
        average_dict.append({'Name': student['Name'], 'Average': round(student['Average'], 2)})  # Round to 2 decimals
    return average_dict

# Step 5: Write the average data into a new text file
def write_averages(file_name, averages):
    logging.info(f"Writing averages to file: {file_name}")
    try:
        with open(file_name, 'w') as file:
            file.write('Name Average\n')  # Header
            for student in averages:
                file.write(f"{student['Name']} {student['Average']}\n")  # Write name and average
        logging.info(f"Successfully wrote averages to {file_name}")
    except Exception as e:
        logging.error(f"Error writing to file {file_name}: {e}")

# Main function to handle the workflow
def main():
    directory = 'grades_files'  # The directory containing the grade files
    grades = read_grades_from_directory(directory)  # Step 1: Read grades
    
    if grades:
        calculate_average(grades)  # Step 3: Calculate averages
        average_dict = create_average_dict(grades)  # Step 4: Prepare the average data
        write_averages('student_average_grades.txt', average_dict)  # Step 5: Write the data to a file
        logging.info("Process completed successfully.")
    else:
        logging.warning("No valid data found to process.")

if __name__ == "__main__":
    main()
