import csv

# Function to save user information and detected symptoms to a CSV file
def save_user_data(user_info, detected_symptom):
    file_name = "user_data.csv"
    
    # Write to CSV file
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_info['name'], user_info['gender'], user_info['age'], detected_symptom])
