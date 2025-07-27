CREATE DATABASE IF NOT EXISTS restaurant;

USE restaurant;


CREATE TABLE IF NOT EXISTS menu_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100),
    description VARCHAR(255),
    price FLOAT,
    category VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    table_number INT,
    total_amount FLOAT
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    item_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);

INSERT INTO menu_items (item_name, description, price, category) VALUES
('Paneer Butter Masala', 'Creamy cottage cheese curry', 250, 'Main Course'),
('Chicken Tikka Masala', 'Spicy chicken curry', 300, 'Main Course'),
('Aloo Paratha', 'Stuffed potato flatbread', 120, 'Main Course'),
('Chole Bhature', 'Chickpeas with fried bread', 150, 'Main Course'),
('Dal Makhani', 'Black lentil curry', 180, 'Main Course'),
('Samosa', 'Fried pastry with spiced potatoes', 60, 'Starter'),
('Pakora', 'Vegetable fritters', 70, 'Starter'),
('Masala Chai', 'Spiced tea', 40, 'Beverage'),
('Rasgulla', 'Spongy syrupy dessert', 90, 'Dessert'),
('Jalebi', 'Deep-fried sweet soaked in syrup', 100, 'Dessert');

INSERT INTO menu_items (item_name, description, price, category) VALUES('poha' ,'nashik-tadka',20,'breakfast');
#-----------
-- 
INSERT INTO menu_items (item_name, description, price, category) VALUES
('Veg Biryani', 'Aromatic rice cooked with fresh vegetables and spices', 220, 'Main Course'),
('Mutton Biryani', 'Spiced rice with tender mutton pieces', 350, 'Main Course'),
('Idli Sambhar', 'Steamed rice cakes with lentil soup', 80, 'Breakfast'),
('Medu Vada', 'Deep-fried savory doughnut made from lentils', 70, 'Breakfast'),
('Butter Naan', 'Soft buttery flatbread', 50, 'Bread'),
('Gulab Jamun', 'Milk-solid-based sweet balls soaked in syrup', 90, 'Dessert'),
('Lassi', 'Chilled sweet yogurt drink', 60, 'Beverage'),
('Cold Coffee', 'Iced coffee with cream', 90, 'Beverage'),
('French Fries', 'Crispy golden potato fries', 100, 'Starter'),
('Pav Bhaji', 'Spiced mashed vegetables served with buns', 130, 'Main Course'),
('Veg Manchurian', 'Fried vegetable balls in spicy sauce', 180, 'Starter'),
('Hakka Noodles', 'Stir-fried noodles with vegetables', 150, 'Main Course'),
('Spring Rolls', 'Fried rolls stuffed with vegetables', 120, 'Starter'),
('Tandoori Chicken', 'Charcoal-grilled spiced chicken', 320, 'Main Course'),
('Chocolate Brownie', 'Rich chocolate dessert', 150, 'Dessert'),
('Fresh Lime Soda', 'Refreshing lemon drink', 50, 'Beverage');




show tables;
select * from orders;
select * from order_items;
select * from menu_items;

