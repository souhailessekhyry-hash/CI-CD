-- Database Schema for Computer Materials Inventory Management System
-- Created for "Les Martial de Informatique" Stock Management

-- Materials table - Main inventory table
CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    brand TEXT,
    model TEXT,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    min_stock INTEGER DEFAULT 5,
    supplier TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories table - Product categories
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

-- Transactions table - Stock movement history
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id INTEGER,
    transaction_type TEXT NOT NULL, -- 'in' for stock in, 'out' for stock out
    quantity INTEGER NOT NULL,
    reason TEXT,
    user TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (material_id) REFERENCES materials (id)
);

-- Suppliers table - Supplier information
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact_person TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table - System users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT DEFAULT 'user', -- 'admin', 'manager', 'user'
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default categories
INSERT OR IGNORE INTO categories (name, description) VALUES 
('Ordinateurs', 'Ordinateurs de bureau et portables'),
('Périphériques', 'Souris, claviers, écrans, imprimantes'),
('Réseau', 'Routeurs, switches, câbles réseau, access points'),
('Stockage', 'Disques durs, SSD, clés USB, cartes mémoire'),
('Logiciels', 'Licences et logiciels informatiques'),
('Accessoires', 'Autres accessoires informatiques'),
('Composants', 'Processeurs, RAM, cartes graphiques, cartes mères'),
('Sécurité', 'Antivirus, pare-feu, systèmes de sécurité');

-- Insert default suppliers
INSERT OR IGNORE INTO suppliers (name, contact_person, phone, email, address) VALUES 
('TechSupply Pro', 'Jean Dupont', '+33 1 23 45 67 89', 'contact@techsupply.fr', '123 Rue de la Tech, Paris'),
('Informatique Plus', 'Marie Martin', '+33 1 98 76 54 32', 'info@informatiqueplus.fr', '456 Avenue des Bits, Lyon'),
('Digital Solutions', 'Pierre Durand', '+33 1 55 44 33 22', 'sales@digitalsolutions.fr', '789 Boulevard du Code, Marseille');

-- Insert sample materials
INSERT OR IGNORE INTO materials (name, category, brand, model, price, quantity, min_stock, supplier, description) VALUES 
('Laptop Dell Inspiron', 'Ordinateurs', 'Dell', 'Inspiron 15 3000', 599.99, 10, 3, 'TechSupply Pro', 'Ordinateur portable 15 pouces, Intel i5, 8GB RAM'),
('Souris Logitech', 'Périphériques', 'Logitech', 'M100', 15.99, 25, 5, 'Informatique Plus', 'Souris optique USB, 1000 DPI'),
('Clavier Mécanique', 'Périphériques', 'Corsair', 'K70 RGB', 149.99, 8, 2, 'Digital Solutions', 'Clavier mécanique RGB, switches Cherry MX'),
('Routeur WiFi', 'Réseau', 'TP-Link', 'Archer C7', 79.99, 12, 4, 'TechSupply Pro', 'Routeur WiFi AC1750, 4 ports Gigabit'),
('SSD Samsung', 'Stockage', 'Samsung', '970 EVO Plus', 89.99, 20, 6, 'Informatique Plus', 'SSD NVMe 500GB, vitesse de lecture 3500 MB/s'),
('Licence Windows 10', 'Logiciels', 'Microsoft', 'Windows 10 Pro', 199.99, 50, 10, 'Digital Solutions', 'Licence Windows 10 Professionnel'),
('Écran 24 pouces', 'Périphériques', 'LG', '24MK430H', 129.99, 15, 3, 'TechSupply Pro', 'Écran LED 24 pouces, Full HD, HDMI'),
('Câble Ethernet', 'Réseau', 'Cat6', 'UTP 5m', 8.99, 100, 20, 'Informatique Plus', 'Câble Ethernet Cat6, 5 mètres'),
('Webcam HD', 'Accessoires', 'Logitech', 'C920', 69.99, 18, 4, 'Digital Solutions', 'Webcam HD 1080p, micro intégré'),
('Antivirus Kaspersky', 'Sécurité', 'Kaspersky', 'Internet Security', 29.99, 30, 8, 'TechSupply Pro', 'Antivirus 1 an, 3 postes');

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_materials_category ON materials(category);
CREATE INDEX IF NOT EXISTS idx_materials_brand ON materials(brand);
CREATE INDEX IF NOT EXISTS idx_materials_supplier ON materials(supplier);
CREATE INDEX IF NOT EXISTS idx_transactions_material_id ON transactions(material_id);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(created_at);
CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(transaction_type);

-- Views for common queries
CREATE VIEW IF NOT EXISTS low_stock_materials AS
SELECT m.*, c.description as category_description
FROM materials m
LEFT JOIN categories c ON m.category = c.name
WHERE m.quantity <= m.min_stock
ORDER BY (m.quantity - m.min_stock) ASC;

CREATE VIEW IF NOT EXISTS stock_value_by_category AS
SELECT 
    m.category,
    COUNT(*) as material_count,
    SUM(m.quantity) as total_quantity,
    SUM(m.price * m.quantity) as total_value,
    AVG(m.price) as avg_price
FROM materials m
GROUP BY m.category
ORDER BY total_value DESC;

CREATE VIEW IF NOT EXISTS recent_transactions AS
SELECT 
    t.*,
    m.name as material_name,
    m.category as material_category
FROM transactions t
JOIN materials m ON t.material_id = m.id
ORDER BY t.created_at DESC
LIMIT 50;
