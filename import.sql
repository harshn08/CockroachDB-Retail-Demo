DROP DATABASE IF EXISTS roachshop_demo;
CREATE DATABASE roachshop_demo;

-- Users Table
CREATE TABLE IF NOT EXISTS roachshop_demo.public.Users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR,
    email VARCHAR UNIQUE,
    password_hash VARCHAR,
    street_address TEXT,
    city VARCHAR,
    state VARCHAR,
    country VARCHAR,
    region VARCHAR,
    zipcode VARCHAR,
    phone_number VARCHAR,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- Categories Table
CREATE TABLE IF NOT EXISTS roachshop_demo.public.Categories (
    category_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_name VARCHAR,
    description TEXT
);

-- Products Table
CREATE TABLE IF NOT EXISTS roachshop_demo.public.Products (
    product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR,
    description TEXT,
    price DECIMAL,
    category_id UUID REFERENCES Categories(category_id),
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- Inventory Table
CREATE TABLE IF NOT EXISTS roachshop_demo.public.Inventory (
    inventory_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES Products(product_id),
    quantity INT,
    warehouse_location VARCHAR,
    region VARCHAR,
    last_updated TIMESTAMP DEFAULT now()
);

-- Orders Table
CREATE TABLE IF NOT EXISTS roachshop_demo.public.Orders (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES Users(user_id),
    order_status VARCHAR,
    total_amount DECIMAL,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- Order Items Table
CREATE TABLE IF NOT EXISTS roachshop_demo.public.Order_Items (
    order_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES Orders(order_id),
    product_id UUID REFERENCES Products(product_id),
    quantity INT,
    price DECIMAL
);

-- Payment Details Table
CREATE TABLE IF NOT EXISTS roachshop_demo.public.Payment_Details (
    payment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES Orders(order_id),
    payment_method VARCHAR,
    payment_status VARCHAR,
    transaction_id VARCHAR,
    amount DECIMAL,
    created_at TIMESTAMP DEFAULT now()
);


-- Cart Table
CREATE TABLE IF NOT EXISTS roachshop_demo.public.Cart (
    cart_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES Users(user_id),
    status VARCHAR CHECK (status IN ('active', 'inactive', 'canceled')) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- Cart_Items Table
CREATE TABLE IF NOT EXISTS roachshop_demo.public.Cart_Items (
    cart_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cart_id UUID REFERENCES Cart(cart_id),
    product_id UUID REFERENCES Products(product_id),
    quantity INT,
    price DECIMAL,
    added_at TIMESTAMP
);
