import psycopg2
import random
import uuid
from datetime import datetime

# Define connection parameters
DB_PARAMS = {
    'host': '',
    'port': '',
    'user': '',
    'password': '',
    'dbname': '<cluster-identifier>.roachshop_demo'
}

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

# Fetch users from the database
def fetch_users():
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT user_id, region FROM Users where region = 'us-west'")
        return cursor.fetchall()

# Fetch products from the database
def fetch_products():
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT product_id, name, price FROM Products")
        return cursor.fetchall()

# Check if a product is in stock for a given quantity
def in_stock(product_id, requested_quantity):
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT SUM(quantity)
            FROM Inventory
            WHERE product_id = %s
            GROUP BY product_id
        """, (product_id,))
        result = cursor.fetchone()
        if result and result[0] >= requested_quantity:
            return True
        return False

# Insert a new cart into the Cart table
def create_cart(user_id):
    cart_id = str(uuid.uuid4())
    with DatabaseConnection() as cursor:
        cursor.execute("""
            INSERT INTO Cart (cart_id, user_id, status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (cart_id, user_id, 'active', random_timestamp(), random_timestamp()))
    return cart_id

# Insert a new cart item into the Cart_Items table
def insert_cart_item(cart_item):
    with DatabaseConnection() as cursor:
        cursor.execute("""
            INSERT INTO Cart_Items (cart_item_id, cart_id, product_id, quantity, price, added_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (cart_item['cart_item_id'], cart_item['cart_id'], cart_item['product_id'], cart_item['quantity'], cart_item['price'], cart_item['added_at']))

# Update the status of a cart in the Cart table
def update_cart_status(cart_id, status):
    with DatabaseConnection() as cursor:
        cursor.execute("""
            UPDATE Cart
            SET status = %s, updated_at = %s
            WHERE cart_id = %s
        """, (status, random_timestamp(), cart_id))

# Insert a new order and order items into the Orders and Order_Items tables
def insert_order(order, order_items):
    with DatabaseConnection() as cursor:
        # Insert order
        cursor.execute("""
            INSERT INTO Orders (order_id, user_id, order_status, total_amount, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (order['order_id'], order['user_id'], order['order_status'], order['total_amount'], order['created_at'], order['updated_at']))

        # Insert order items
        for item in order_items:
            cursor.execute("""
                INSERT INTO Order_Items (order_item_id, order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s, %s)
            """, (item['order_item_id'], item['order_id'], item['product_id'], item['quantity'], item['price']))

# Insert payment details into the Payment_Details table
def insert_payment_details(payment):
    with DatabaseConnection() as cursor:
        cursor.execute("""
            INSERT INTO Payment_Details (payment_id, order_id, payment_method, payment_status, transaction_id, amount, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (payment['payment_id'], payment['order_id'], payment['payment_method'], payment['payment_status'], payment['transaction_id'], payment['amount'], payment['created_at']))

# Update inventory after an order
def update_inventory(product_id, quantity):
    with DatabaseConnection() as cursor:
        cursor.execute("""
            UPDATE Inventory
            SET quantity = quantity - %s, last_updated = %s
            WHERE product_id = %s
        """, (quantity, random_timestamp(), product_id))

# Simulate adding items to the cart
def simulate_add_to_cart(user):
    cart_id = create_cart(user[0])
    cart_items = []
    num_items = random.randint(1, 5)
    for _ in range(num_items):
        product = random.choice(products)
        quantity = random.randint(1, 3)

        if in_stock(product[0], quantity):
            cart_item = {
                'cart_item_id': str(uuid.uuid4()),
                'cart_id': cart_id,
                'product_id': product[0],
                'quantity': quantity,
                'price': product[2],
                'added_at': random_timestamp()
            }
            insert_cart_item(cart_item)
            cart_items.append(cart_item)
        else:
            print("Product {} is out of stock for the requested quantity {}.".format(product[1], quantity))
    
    return cart_id, cart_items

# Simulate the checkout process
def simulate_checkout(cart_id, cart_items, user):
    order_id = str(uuid.uuid4())
    total_amount = sum(item['price'] * item['quantity'] for item in cart_items)
    order_status = 'completed' if random.random() > 0.1 else 'canceled'
    order = {
        'order_id': order_id,
        'user_id': user[0],
        'order_status': order_status,
        'total_amount': total_amount,
        'created_at': random_timestamp(),
        'updated_at': random_timestamp()
    }

    order_items = [{
        'order_item_id': str(uuid.uuid4()),
        'order_id': order_id,
        'product_id': item['product_id'],
        'quantity': item['quantity'],
        'price': item['price']
    } for item in cart_items]

    if order_status == 'completed':
        insert_order(order, order_items)
        simulate_payment(order)
        update_cart_status(cart_id, 'inactive')
    else:
        update_cart_status(cart_id, 'canceled')
    return order, order_items

# Simulate payment process
def simulate_payment(order):
    payment_id = str(uuid.uuid4())
    payment_method = random.choice(['credit card', 'paypal'])
    payment_status = 'completed' if random.random() > 0.05 else 'failed'  # 95% chance of successful payment
    transaction_id = str(uuid.uuid4()) if payment_status == 'completed' else None
    payment = {
        'payment_id': payment_id,
        'order_id': order['order_id'],
        'payment_method': payment_method,
        'payment_status': payment_status,
        'transaction_id': transaction_id,
        'amount': order['total_amount'],
        'created_at': random_timestamp()
    }
    insert_payment_details(payment)

# Update inventory based on the completed order
def process_order(user, order_items):
    for item in order_items:
        update_inventory(item['product_id'], item['quantity'])

'''

# Run the simulation
def run_simulation():
    global products
    users = fetch_users()
    products = fetch_products()

    for user in users:
        for _ in range(random.randint(1, 5)):  # Simulate 1 to 5 interactions per user
            cart_id, cart_items = simulate_add_to_cart(user)
            if not cart_items:
                update_cart_status(cart_id, 'canceled')  # Mark the cart as canceled if no items are added
                continue  # Skip if no items were added to the cart due to stock issues
            order, order_items = simulate_checkout(cart_id, cart_items, user)
            if order['order_status'] == 'completed':
                process_order(user, order_items)
            print("User {} from {} placed an order {} with status {}.".format(user[0], user[1], order['order_id'], order['order_status']))

'''

# Run the simulation in random order

def run_simulation():
    global products
    users = fetch_users()
    products = fetch_products()
    
    # Prepare a queue of users with at least 5 orders each
    order_queue = []
    for user in users:
        for _ in range(5):
            order_queue.append(user)

    # Shuffle the initial order queue to randomize user order
    random.shuffle(order_queue)

    # Ensure no user places more than 2 consecutive orders
    while order_queue:
        # Select the next user and ensure no more than 2 consecutive orders
        current_user = order_queue.pop(0)
        consecutive_orders = 1
        
        # Place the first order
        cart_id, cart_items = simulate_add_to_cart(current_user)
        if not cart_items:
            update_cart_status(cart_id, 'canceled')
        else:
            order, order_items = simulate_checkout(cart_id, cart_items, current_user)
            if order['order_status'] == 'completed':
                process_order(current_user, order_items)
            print("User {} from {} placed an order {} with status {}.".format(current_user[0], current_user[1], order['order_id'], order['order_status']))

        # Place up to one more consecutive order for the current user
        while consecutive_orders < 2 and order_queue and order_queue[0] == current_user:
            order_queue.pop(0)
            cart_id, cart_items = simulate_add_to_cart(current_user)
            if not cart_items:
                update_cart_status(cart_id, 'canceled')
            else:
                order, order_items = simulate_checkout(cart_id, cart_items, current_user)
                if order['order_status'] == 'completed':
                    process_order(current_user, order_items)
                print("User {} from {} placed an order {} with status {}.".format(current_user[0], current_user[1], order['order_id'], order['order_status']))
            consecutive_orders += 1

        # Shuffle remaining order_queue to ensure randomness in subsequent picks
        random.shuffle(order_queue)

# Execute the simulation
run_simulation()
