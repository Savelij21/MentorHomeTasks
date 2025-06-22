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


/*
 Этап 2: Установка индексов
 */

CREATE INDEX idx__orders__customer_id ON orders(customer_id);
CREATE INDEX idx__order_items__order_id__price ON order_items(order_id, price);
CREATE INDEX idx__order_items__product_name ON order_items(product_name);


/*
 Этап 3: Анализ использования индексов
 */


EXPLAIN ANALYZE SELECT * FROM order_items
WHERE price > 10000 AND order_id = 123;
-- Index Scan using idx__order_items__order_id__price on order_items


EXPLAIN ANALYZE SELECT * FROM orders
WHERE customer_id = 1;
-- Seq Scan on orders


/*
 Этап 4: Удаление неэффективных индексов

??? Я так понял, что лишние индексы нужно выделить именно для наших запросов в пред. этапе ???
 */


DROP INDEX idx__orders__customer_id;
-- При наших данных во-первых - в целом таблица orders небольшая (6 заказов), поэтому последовательный поиск проще,
-- а во-вторых - низкая селективность, так как много неуникальных записей в столбце (всего 3 покупателя)

DROP INDEX idx__order_items__product_name;
-- Во-первых - у нас не было запроса с использованием этого поля, а даже если бы и был - мы предполагаем, что
-- всего у нас 500 возможных именно товаров (Товар 1 - Товар 500). В отношении к 10_000_000 товаров это низкая
-- селективность, поэтому индекс будет практически бесполезен. Все равно будет много последовательного перебора.


/*
 Этап 5: Бизнес-логика с использованием транзакций

Цель: Обеспечить целостность данных при выполнении операций.

Сценарий:
 Реализовать следующую логику в виде SQL-транзакции: Клиент оформляет заказ, который включает в себя:
 - Создание новой записи в таблице orders с текущей датой.
 - Добавление 3–5 случайных товаров в таблицу order_items для созданного заказа.
 - В случае любой ошибки (например, попытка вставить NULL в product_name), вся транзакция откатывается.

Требование:
 - Использовать явное начало/конец транзакции (BEGIN, COMMIT, ROLLBACK).
 - Обработать возможные ошибки.
 - Продемонстрировать, что в случае сбоя никаких частичных данных не остаётся в базе.

 */

BEGIN;  -- Корректный запрос

    with new_order AS (
        INSERT INTO orders (customer_id, order_date) VALUES (3, current_date)
        RETURNING id
    )

    INSERT INTO order_items (order_id, product_name, quantity, price) VALUES
        ((SELECT id FROM new_order), 'TestProduct1', 1, 100),
        ((SELECT id FROM new_order), 'TestProduct2', 2, 200);

COMMIT;


BEGIN;  -- Запрос с ошибкой и ручным роллбэком

    with new_order AS (
        INSERT INTO orders (customer_id, order_date) VALUES (3, current_date)
        RETURNING id
    )

    INSERT INTO order_items (order_id, product_name, quantity, price) VALUES
        ((SELECT id FROM new_order), 'TestProduct3', 3, 300),
        ((SELECT id FROM new_order), NULL, 4, 400);

ROLLBACK;

-- Проверка, что новая запись заказа не создалась (в таблице только один заказ с текущей датой)
SELECT customer_id, order_date FROM orders
WHERE customer_id = 3 AND order_date = current_date
ORDER BY order_date DESC;

-- Проверка, что новые товары не остались в БД (проверка по товару, добавленному с названием)
SELECT * FROM order_items
WHERE product_name = 'TestProduct3';
