from tinydb import TinyDB, Query
from datetime import datetime
import random

# Initialize the database
db = TinyDB('users_db.json')

# Function to generate a fake reservation code and flight code
def generate_code(prefix, length=6):
    return prefix + ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))

# Function to create a user entry
def create_user_entry(name, country_origin):

    if name == "Ruy Cabello":
        return {
            'user_name': name, 
            'country_origin': 'Mexico',
            'reservation_date': 'Tuesday, October 29',
            'reservation_code': 'AB294',
            'flight_code': 'EK352'
        }
    
    reservation_date = datetime.now().strftime('%Y-%m-%d')
    reservation_code = generate_code('RES')
    flight_code = generate_code('FL')

    return {
        'user_name': name,
        'country_origin': country_origin,
        'reservation_date': reservation_date,
        'reservation_code': reservation_code,
        'flight_code': flight_code
    }

# Add fake users to the database
users = [
    create_user_entry('Ruy Cabello', 'Mexico'),
    create_user_entry('Alice Johnson', 'United States'),
    create_user_entry('Liam Wong', 'Canada'),
    create_user_entry('Sofia Garcia', 'Spain'),
    create_user_entry('Carlos Silva', 'Brazil')
]

# Insert users into the database
db.insert_multiple(users)

# Query the database to display users
User = Query()
print(db.all())
