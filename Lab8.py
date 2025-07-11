
import bcrypt 
import os 
 
# File to store user data 
USER_FILE = 'users.txt' 
 
# Function to register a new user 
def register_user(): 
    username = input("Enter a unique username: ") 
     
    # Check if the username already exists 
    if username_exists(username): 
        print("Username already exists. Please choose another one.") 
        return 
 
    password = input("Enter a password: ").encode('utf-8') 
     
    # Hash the password with bcrypt 
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()) 
 
    # Store the username and hashed password in the file 
    with open(USER_FILE, 'a') as file: 
        file.write(f"{username},{hashed_password.decode('utf-8')}\n") 
     
    print("Registration successful!") 
 
# Function to check if a username exists in the file 
def username_exists(username): 
    if not os.path.exists(USER_FILE): 
        return False 
 
    with open(USER_FILE, 'r') as file: 
        for line in file: 
            stored_username, _ = line.strip().split(',') 
            if stored_username == username: 
                return True 
    return False 
 
# Function to log in a user 
def login_user(): 
    username = input("Enter your username: ") 

 
    password = input("Enter your password: ").encode('utf-8') 
     
    # Check if the username exists and get the stored hash 
    stored_hash = get_stored_hash(username) 
    if not stored_hash: 
        print("Username not found.") 
        return 
 
    # Verify the password against the stored hash 
    if bcrypt.checkpw(password, stored_hash.encode('utf-8')): 
        print("Login successful!") 
    else: 
        print("Incorrect password.") 
 
# Function to get the stored hash for a username 
def get_stored_hash(username): 
    if not os.path.exists(USER_FILE): 
        return None 
 
    with open(USER_FILE, 'r') as file: 
        for line in file: 
            stored_username, stored_hash = line.strip().split(',') 
            if stored_username == username: 
                return stored_hash 
    return None 
 
# Main function to drive the program 
def main(): 
    while True: 
        print("\nName:Patel Honey Ashishkumar") 
        print("\nRoll number:22BCP402") 
        print("\nUser Management System") 
        print("1. Register") 
        print("2. Login") 
        print("3. Exit") 
        choice = input("Choose an option: ") 
 
        if choice == '1': 
            register_user() 
        elif choice == '2': 
            login_user() 
        elif choice == '3': 
            print("Exiting the program.") 
            break 
        else: 
            print("Invalid choice. Please try again.") 
 
if __name__ == "__main__": 
    main() 