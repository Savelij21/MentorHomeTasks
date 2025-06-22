/*
 Prepare the database
 */
DROP TABLE IF EXISTS order_items, orders, customers;


/*
 Этап 1: Создание структуры базы данных
 */

CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

/*
 Этап 2: Наполнение тестовыми данными
 */

INSERT INTO customers (name, email) VALUES
    ('Иван Иванов', 'ivan@example.com'),
    ('Alex', 'alex@example.com'),
    ('Anny', 'anny@example.com');

INSERT INTO orders (customer_id, order_date) VALUES
    (1, '2022-01-01'),
    (1, '2022-02-02'),
    (1, '2022-03-03'),
    (2, '2022-04-04'),
    (2, '2022-05-05'),
    (3, '2022-06-06');

INSERT INTO order_items (order_id, product_name, quantity, price) VALUES
    (1, 'Book', 1, 12000),
    (1, 'Pen', 2, 200),
    (1, 'Pencil', 3, 100),
    (2, 'Shirt', 1, 3000),
    (2, 'Shoes', 3, 4000),
    (3, 'Spoon', 6, 500),
    (3, 'Fork', 3, 600),
    (4, 'Toy', 2, 1000),
    (4, 'Ball', 1, 1400),
    (5, 'Camera', 1, 12000),
    (5, 'Phone', 1, 24000),
    (6, 'Notebook', 1, 50000);


/*
 Этап 3: Запросы на чтение
 */

SELECT orders.id, orders.order_date FROM orders
    JOIN customers on orders.customer_id = customers.id
WHERE customers.name = 'John';


SELECT product_name, quantity, price FROM order_items
WHERE order_id = 2
ORDER BY price DESC;


SELECT customers.name, SUM(order_items.price * order_items.quantity) AS total_spent FROM customers
    JOIN orders ON customers.id = orders.customer_id
    JOIN order_items ON orders.id = order_items.order_id
GROUP BY customers.id
HAVING SUM(order_items.price * order_items.quantity) > 5000;









