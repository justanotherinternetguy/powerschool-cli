from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
import os
import time

load_dotenv()
USERNAME = os.getenv('usern')
PASSWORD = os.getenv('passw')

print("username: ", USERNAME)
# print("password: ", PASSWORD)

driver = webdriver.Chrome()
driver.get("https://millburn.powerschool.com/public/")

text_box = driver.find_element(By.ID, 'fieldAccount')
text_box.send_keys(USERNAME)

text_box = driver.find_element(By.ID, 'fieldPassword')
text_box.send_keys(PASSWORD)

button = driver.find_element(By.ID, 'btn-enter-sign-in')
button.click()

html_content = driver.page_source
# print(html_content)
print('testing')

soup = BeautifulSoup(html_content, 'html.parser')

# Find all <tr> elements with id starting with "ccid_"
class_rows = soup.find_all('tr', id=lambda x: x and x.startswith('ccid_'))

# Initialize a dictionary to store class names and cleaned grades
class_data = {}

# Function to clean grades array
def clean_grades(grades):
    cleaned_grades = []
    for grade in grades:
        # Remove non-numeric characters
        cleaned_grade = re.sub(r'[^0-9]', '', grade)
        # Add to cleaned grades if it's not empty
        if cleaned_grade:
            cleaned_grades.append(cleaned_grade)
    return cleaned_grades

# Iterate through each class row to extract name and grades
for row in class_rows:
    # Get the class name
    class_name_elem = row.find('td', class_='table-element-text-align-start')
    if class_name_elem:
        class_name = ''.join(class_name_elem.find_all(string=True, recursive=False)).strip()
        
        # Initialize an empty list for grades associated with this class
        grades = []
        
        # Get all grades associated with the class
        grade_links = row.find_all('a', class_='bold', href=lambda x: x and x.startswith('scores.html?'))
        for link in grade_links:
            grade_text = link.get_text(strip=True)
            grades.append(grade_text)
        
        # Clean the grades array
        cleaned_grades = clean_grades(grades)
        
        # Store the class name and cleaned grades in the dictionary
        class_data[class_name] = cleaned_grades

# Filter out classes with names containing "Guidance" or "Phys Ed" but retain the key if the name has "AP" in it
filtered_class_data = {class_name: grades for class_name, grades in class_data.items()
                       if 'Guidance' not in class_name and 'Phys Ed' not in class_name or 'AP' in class_name}

# Define a mapping for the labels based on the number of grades
label_mapping = {
    4: ["Q1", "Q2", "Q3", "Q4"],        # Mapping for 4 grades
    5: ["Q1", "Q2", "X1", "Q3", "Q4"],  # Mapping for 5 grades
    6: ["Q1", "Q2", "X1", "X2", "Q3", "Q4"]  # Mapping for 6 grades
}

# Print class names and cleaned grades after filtering
for class_name, grades in filtered_class_data.items():
    print(f"Class: {class_name}")
    
    # Determine the number of grades available
    num_grades = len(grades)
    
    # Get the label mapping based on the number of grades available
    labels = label_mapping.get(num_grades, [f"Grade {i+1}" for i in range(num_grades)])
    
    # Print available grades with labels
    for label, grade in zip(labels, grades):
        print(f"{label}: {grade}")
    
    print()  # Print an empty line for separation



while True:
    pass