import os  
import shutil  
# Custom exceptions  
class FileNotFoundError(Exception):  
    def __init__(self, message="Input file not found. Please check the file path and try again."):  
            self.message = message  
            super().__init__(self.message)  
class InvalidInputDataError(Exception):  
    def __init__(self, message="Invalid input data encountered during processing."):  
            self.message = message  
            super().__init__(self.message)  
class DiskSpaceFullError(Exception):  
    def __init__(self, message="Insufficient disk space to write the output file."):  
            self.message = message  
            super().__init__(self.message)  

 
  
# Function to read input from a file  
def read_input(file_path):  
    try:  
        if not os.path.exists(file_path):  
            raise FileNotFoundError  
        with open(file_path, 'r') as file:  
            data = file.read()  
            if not isinstance(data, str) or len(data.strip()) == 0:  
                raise InvalidInputDataError  
            return data  
    except FileNotFoundError as e:  
        print(f"Error: {e}")  
        return None  
    except InvalidInputDataError as e:  
        print(f"Error: {e}")  
        return None  
  
# Function to process the text data  
def process_text(data):  
    try:  
        word_count = len(data.split())  
        char_frequencies = {char: data.count(char) for char in set(data)}  
        return word_count, char_frequencies  
    except Exception as e:  
        print(f"Error during processing: {e}")  
        raise InvalidInputDataError  
  
# Function to check disk space and write the results to an output file  
def write_output(output_file, word_count, char_frequencies):  
    try:  
        # Check disk space using shutil.disk_usage()  
        total, used, free = shutil.disk_usage(os.path.dirname(output_file))  
  
  
        if free < 1024:  # Check if at least 1 KB is free  
            raise DiskSpaceFullError  
          
        with open(output_file, 'w') as file:  
            file.write(f"Word Count: {word_count}\n")  
            file.write("Character Frequencies:\n")  
            for char, freq in char_frequencies.items():  
                file.write(f"{char}: {freq}\n")  
    except DiskSpaceFullError as e:  
        print(f"Error: {e}")  
    except Exception as e:  
        print(f"Unexpected error during file write: {e}")  
  
# Main program flow  
def main():  
    input_file = input("Enter the input file path: ")  
    output_file = input("Enter the output file path: ")  
  
data = read_input(input_file)  
if data:  
    try:  
        word_count, char_frequencies = process_text(data)  
        write_output(output_file, word_count, char_frequencies)  
 
        print("Processing complete and results saved to the output file.")  
    except InvalidInputDataError as e:  
        print(f"Error: {e}")  
    except DiskSpaceFullError as e:  
        print(f"Error: {e}")  
if __name__ == "__main__":  
    main() 