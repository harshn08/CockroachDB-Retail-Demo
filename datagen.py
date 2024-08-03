import psycopg2
import random
import uuid
from datetime import datetime
from faker import Faker

# Define connection parameters
DB_PARAMS = {
    'host': '',
    'port': '',
    'user': '',
    'password': '',
    'dbname': '<cluster-identifier>.roachshop_demo'
}

fake = Faker()

# Function to generate a random timestamp
def random_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Database connection context manager
class DatabaseConnection:
    def __enter__(self):
        self.conn = psycopg2.connect(**DB_PARAMS)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

# Expanded region-specific data
regions_data = {
    'us-west': {
        'states': ['California', 'Washington', 'Oregon', 'Nevada', 'Arizona', 'Utah'],
        'cities_zip': {
            'California': ['Los Angeles', 'San Francisco', 'San Diego', 'Sacramento'],
            'Washington': ['Seattle', 'Spokane', 'Tacoma', 'Vancouver'],
            'Oregon': ['Portland', 'Eugene', 'Salem', 'Bend'],
            'Nevada': ['Las Vegas', 'Reno', 'Henderson', 'Carson City'],
            'Arizona': ['Phoenix', 'Tucson', 'Mesa', 'Chandler'],
            'Utah': ['Salt Lake City', 'Provo', 'Ogden', 'St. George']
        }
    },
    'us-east': {
        'states': ['New York', 'Massachusetts', 'Virginia', 'Florida', 'Pennsylvania', 'Georgia'],
        'cities_zip': {
            'New York': ['New York City', 'Buffalo', 'Rochester', 'Albany'],
            'Massachusetts': ['Boston', 'Worcester', 'Springfield', 'Cambridge'],
            'Virginia': ['Richmond', 'Norfolk', 'Arlington', 'Charlottesville'],
            'Florida': ['Miami', 'Orlando', 'Tampa', 'Jacksonville'],
            'Pennsylvania': ['Philadelphia', 'Pittsburgh', 'Allentown', 'Erie'],
            'Georgia': ['Atlanta', 'Savannah', 'Augusta', 'Columbus']
        }
    },
    'us-central': {
        'states': ['Illinois', 'Texas', 'Ohio', 'Michigan', 'Missouri', 'Minnesota'],
        'cities_zip': {
            'Illinois': ['Chicago', 'Springfield', 'Peoria', 'Naperville'],
            'Texas': ['Houston', 'Dallas', 'Austin', 'San Antonio'],
            'Ohio': ['Columbus', 'Cleveland', 'Cincinnati', 'Toledo'],
            'Michigan': ['Detroit', 'Grand Rapids', 'Warren', 'Lansing'],
            'Missouri': ['Kansas City', 'St. Louis', 'Springfield', 'Columbia'],
            'Minnesota': ['Minneapolis', 'St. Paul', 'Rochester', 'Duluth']
        }
    }
}

category_data = [
    ('Electronics', 'Devices and gadgets like smartphones, tablets, laptops, and other electronic equipment.'),
    ('Clothing', 'Apparel for men, women, and children including shirts, pants, dresses, and outerwear.'),
    ('Home & Kitchen', 'Furniture, kitchenware, and home decor items for everyday use.'),
    ('Books', 'A wide variety of books including fiction, non-fiction, textbooks, and more.'),
    ('Toys & Games', 'Toys, board games, and puzzles for kids and adults.')
]

# Predefined product data corresponding to categories
product_data = {
    'Electronics': [
        ('Smartphone', 'A high-end smartphone with a large display and powerful processor.'),
        ('Laptop', 'A sleek and portable laptop with ample storage and fast performance.'),
        ('Headphones', 'Noise-cancelling over-ear headphones with superior sound quality.'),
        ('Smartwatch', 'A stylish smartwatch with fitness tracking and notification features.')
    ],
    'Clothing': [
        ('T-shirt', 'A comfortable cotton T-shirt available in various colors and sizes.'),
        ('Jeans', 'Denim jeans with a classic fit and durable material.'),
        ('Jacket', 'A warm and stylish jacket suitable for cold weather.'),
        ('Dress', 'An elegant dress perfect for special occasions.')
    ],
    'Home & Kitchen': [
        ('Sofa', 'A spacious and comfortable sofa with a modern design.'),
        ('Coffee Maker', 'A quick and efficient coffee maker for your daily brew.'),
        ('Cookware Set', 'A complete set of non-stick cookware for all your cooking needs.'),
        ('Blender', 'A powerful blender for smoothies, soups, and more.')
    ],
    'Books': [
        ('Mystery Novel', 'A gripping mystery novel that keeps you on the edge of your seat.'),
        ('Science Fiction', 'A science fiction novel set in a futuristic world.'),
        ('Cookbook', 'A cookbook with a collection of delicious recipes.'),
        ('Self-Help', 'A self-help book with tips for personal growth and success.')
    ],
    'Toys & Games': [
        ('Board Game', 'A fun and strategic board game for family and friends.'),
        ('Action Figure', 'A collectible action figure from a popular franchise.'),
        ('Puzzle', 'A challenging puzzle with 1000 pieces.'),
        ('Building Blocks', 'A set of colorful building blocks for creative play.')
    ]
}

# Insert a user into the Users table
def insert_user(user):
    with DatabaseConnection() as cursor:
        cursor.execute("""
            INSERT INTO Users (user_id, name, email, password_hash, street_address, city, state, country, region, zipcode, phone_number, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user['user_id'], user['name'], user['email'], user['password_hash'], user['street_address'], user['city'], user['state'], user['country'], user['region'], user['zipcode'], user['phone_number'], user['created_at'], user['updated_at']))

# Insert a category into the Categories table
def insert_category(category):
    with DatabaseConnection() as cursor:
        cursor.execute("""
            INSERT INTO Categories (category_id, category_name, description)
            VALUES (%s, %s, %s)
        """, (category['category_id'], category['category_name'], category['description']))

# Insert a product into the Products table
def insert_product(product):
    with DatabaseConnection() as cursor:
        cursor.execute("""
            INSERT INTO Products (product_id, name, description, price, category_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (product['product_id'], product['name'], product['description'], product['price'], product['category_id'], product['created_at'], product['updated_at']))

# Insert inventory into the Inventory table
def insert_inventory(inventory_item):
    with DatabaseConnection() as cursor:
        cursor.execute("""
            INSERT INTO Inventory (inventory_id, product_id, quantity, warehouse_location, region, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (inventory_item['inventory_id'], inventory_item['product_id'], inventory_item['quantity'], inventory_item['warehouse_location'], inventory_item['region'], inventory_item['last_updated']))

# Generate Users
users = []
for region in regions_data.keys():
    for state in regions_data[region]['states']:
        for city in regions_data[region]['cities_zip'][state]:
            num_users = random.randint(5, 10)  # At least 5 and at most 10 users per city
            for _ in range(num_users):
                user = {
                    'user_id': str(uuid.uuid4()),
                    'name': fake.name(),
                    'email': fake.email(),
                    'password_hash': fake.sha256(),
                    'street_address': fake.street_address(),
                    'city': city,
                    'state': state,
                    'country': 'United States',
                    'region': region,
                    'zipcode': fake.zipcode(),
                    'phone_number': fake.phone_number(),
                    'created_at': random_timestamp(),
                    'updated_at': random_timestamp()
                }
                insert_user(user)
                users.append(user)

'''
# Generate Users
users = []
for _ in range(10):
    region = random.choice(list(regions_data.keys()))
    state = random.choice(regions_data[region]['states'])
    city = random.choice(regions_data[region]['cities_zip'][state])
    user = {
        'user_id': str(uuid.uuid4()),
        'name': fake.name(),
        'email': fake.email(),
        'password_hash': fake.sha256(),
        'street_address': fake.street_address(),
        'city': city,
        'state': state,
        'country': 'United States',
        'region': region,
        'zipcode': fake.zipcode(),
        'phone_number': fake.phone_number(),
        'created_at': random_timestamp(),
        'updated_at': random_timestamp()
    }
    insert_user(user)
    users.append(user)


# Generate Categories

categories = []
for _ in range(5):
    category = {
        'category_id': str(uuid.uuid4()),
        'category_name': fake.word(),
        'description': fake.text()
    }
    insert_category(category)
    categories.append(category)

# Generate Products
products = []
for _ in range(20):
    category = random.choice(categories)
    product = {
        'product_id': str(uuid.uuid4()),
        'name': fake.word(),
        'description': fake.text(),
        'price': round(random.uniform(10.0, 100.0), 2),
        'category_id': category['category_id'],
        'created_at': random_timestamp(),
        'updated_at': random_timestamp()
    }
    insert_product(product)
    products.append(product)
'''
# Generate Categories
categories = []
for category_name, description in category_data:
    category = {
        'category_id': str(uuid.uuid4()),
        'category_name': category_name,
        'description': description
    }
    insert_category(category)
    categories.append(category)

# Generate Products
products = []
for category in categories:
    category_name = category['category_name']
    for product_name, product_description in product_data[category_name]:
        product = {
            'product_id': str(uuid.uuid4()),
            'name': product_name,
            'description': product_description,
            'price': round(random.uniform(10.0, 100.0), 2),
            'category_id': category['category_id'],
            'created_at': random_timestamp(),
            'updated_at': random_timestamp()
        }
        insert_product(product)
        products.append(product)

# Generate Inventory
inventory_items = []
warehouses = {}  # Dictionary to track products per warehouse

# Create a list of warehouses based on regions and cities
all_warehouses = []
for region in regions_data.keys():
    for state in regions_data[region]['states']:
        for city in regions_data[region]['cities_zip'][state]:
            warehouse_key = "{}, {}".format(city, state)
            all_warehouses.append((warehouse_key, region))

# Distribute products across all warehouses
for product in products:
    num_warehouses = random.randint(1, 3)  # Randomly choose how many warehouses to store the product
    selected_warehouses = random.sample(all_warehouses, num_warehouses)
    for warehouse_key, region in selected_warehouses:
        if warehouse_key not in warehouses:
            warehouses[warehouse_key] = []
        warehouses[warehouse_key].append(product['product_id'])

        inventory_item = {
            'inventory_id': str(uuid.uuid4()),
            'product_id': product['product_id'],
            'quantity': random.randint(10000, 50000),
            'warehouse_location': warehouse_key.split(", ")[0],
            'region': region,
            'last_updated': random_timestamp()
        }
        insert_inventory(inventory_item)
        inventory_items.append(inventory_item)


'''
# Generate Inventory
inventory_items = []
for product in products:
    region = random.choice(list(regions_data.keys()))
    state = random.choice(regions_data[region]['states'])
    city = random.choice(regions_data[region]['cities_zip'][state])
    inventory_item = {
        'inventory_id': str(uuid.uuid4()),
        'product_id': product['product_id'],
        'quantity': random.randint(100, 1000),
        'warehouse_location': city,
        'region': region,
        'last_updated': random_timestamp()
    }
    insert_inventory(inventory_item)
    inventory_items.append(inventory_item)
'''

print("Data generation and insertion completed.")
