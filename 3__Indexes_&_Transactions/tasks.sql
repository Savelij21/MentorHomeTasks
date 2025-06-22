/*
 Этап 1: Массовое наполнение базы
 */

INSERT INTO order_items (order_id, product_name, quantity, price)
SELECT
    (SELECT id FROM orders ORDER BY random() LIMIT 1) AS order_id,  -- случайный заказ
    'Товар ' || (trunc(random() * 500) + 1)::int AS product_name,   -- от "Товар 1" до "Товар 500"
    (trunc(random() * 10) + 1)::int AS quantity,                    -- количество от 1 до 10
    (trunc(random() * 100000) + 100)::int                           -- цена от 100 до 100_000
FROM generate_series(1, 1000000);







