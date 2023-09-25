import json
from faker import Faker
import random
import os

# https://faker.readthedocs.io/en/master/
# "Faker is a Python package that generates fake data for you."
fake = Faker()

# amount of records to add
num_new_records = 50

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EMPLOYEE_JSON =  os.path.join(CURRENT_DIR, "employees.json")

# open employees.json
with open(EMPLOYEE_JSON, 'r') as file:
    data = json.load(file)

# grabbing last UID from json
last_uid = data['employees'][-1]['uid']

# creation of fake employees
def generate_employee(uid):
    skills_list = [
    'Python', 'JavaScript', 'Fishing', 'Boating', 'Sailing', 'Swimming', 'R', 'SQL', 'HTML', 'CSS',
    'Data Analysis', 'Graphic Design', 'Public Speaking', 'Photography', 'Machine Learning',
    'Mobile App Development', 'Event Planning', 'Floral Design', 'Copywriting', 'Search Engine Optimization (SEO)',
    'Digital Marketing', '3D Modeling', 'Network Security', 'Welding', 'Cloud Computing',
    'Game Development', 'Robotics', 'E-commerce Management', 'Foreign Language Translation', 'Music Production']
    skills = ', '.join(random.sample(skills_list, random.randint(1, 5)))

    return {
        "uid": uid,
        "name": fake.name(),
        "position": fake.job(),
        "ssn": fake.ssn(),
        "address": fake.address().replace('\n', ', '),
        "email": fake.email(),
        "phonenumber": fake.numerify(text='###-###-####'), # need to use this because fake.phonenumber gives numbers
        "skills": skills                                   # from across the world and some have weird formatting
    }

# add new fake records
for i in range(1, num_new_records + 1):
    data['employees'].append(generate_employee(last_uid + i))

# saving
with open(EMPLOYEE_JSON, 'w') as file:
    json.dump(data, file, indent=4)

print(f"Added {num_new_records} new employee records")
