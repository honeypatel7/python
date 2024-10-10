import csv

# Step 1: Read the data from "student_grades.csv"
def read_grades(file_name):
    with open(file_name, mode='r') as file:
        reader = csv.DictReader(file)
        grades = []
        for row in reader:
            grades.append({
                'Name': row['Name'],
                'Maths': float(row['Maths']),
                'Science': float(row['Science']),
                'English': float(row['English'])
            })
    return grades

# Step 3: Create average function to calculate the average for each student
def calculate_average(grades):
    for student in grades:
        student['Average'] = (student['Maths'] + student['Science'] + student['English']) /3
        

# Step 4: Store the student's name and their corresponding average score in a new dictionary
def create_average_dict(grades):
    average_dict = []
    for student in grades:
        average_dict.append({'Name': student['Name'], 'Average': round(student['Average'], 2)})
    return average_dict

# Step 5: Write the data from the dictionary into a new CSV file
def write_averages(file_name, averages):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Name', 'Average'])
        writer.writeheader()
        for student in averages:
            writer.writerow(student)

# Main function
def main():
    grades = read_grades('student_grades.csv')
    calculate_average(grades)
    average_dict = create_average_dict(grades)
    write_averages('student_average_grades.csv', average_dict)
    print("Average grades have been written to 'student_average_grades.csv'")
if __name__ == "__main__":
    main()
