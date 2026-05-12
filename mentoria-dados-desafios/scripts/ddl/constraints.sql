-- Arquivo: scripts/ddl/constraints.sql
-- Adição de Foreign Keys e Checks

-- Foreign Keys
ALTER TABLE orders 
    ADD CONSTRAINT fk_orders_customers 
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT;

ALTER TABLE order_items 
    ADD CONSTRAINT fk_order_items_orders 
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE;

ALTER TABLE order_items 
    ADD CONSTRAINT fk_order_items_products 
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT;

ALTER TABLE payments 
    ADD CONSTRAINT fk_payments_orders 
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE;

ALTER TABLE shipments 
    ADD CONSTRAINT fk_shipments_orders 
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE;

-- Check Constraints
ALTER TABLE products 
    ADD CONSTRAINT chk_products_price CHECK (price >= 0),
    ADD CONSTRAINT chk_products_cost CHECK (cost >= 0);

ALTER TABLE order_items 
    ADD CONSTRAINT chk_order_items_qty CHECK (quantity > 0),
    ADD CONSTRAINT chk_order_items_price CHECK (unit_price >= 0);

ALTER TABLE payments 
    ADD CONSTRAINT chk_payments_amount CHECK (amount >= 0);

ALTER TABLE customers 
    ADD CONSTRAINT chk_customers_status CHECK (status IN ('active', 'inactive'));

ALTER TABLE orders 
    ADD CONSTRAINT chk_orders_status CHECK (status IN ('pending', 'paid', 'cancelled', 'refunded'));

ALTER TABLE payments 
    ADD CONSTRAINT chk_payments_status CHECK (status IN ('pending', 'completed', 'failed', 'refunded'));

ALTER TABLE shipments 
    ADD CONSTRAINT chk_shipments_status CHECK (status IN ('pending', 'shipped', 'delivered', 'returned'));
