from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Database configuration
DATABASE = 'inventory.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create materials table
    cursor.execute('''
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
        )
    ''')
    
    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER,
            transaction_type TEXT NOT NULL, -- 'in' or 'out'
            quantity INTEGER NOT NULL,
            reason TEXT,
            user TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (material_id) REFERENCES materials (id)
        )
    ''')
    
    # Create categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    ''')
    
    # Insert default categories
    default_categories = [
        ('Ordinateurs', 'Ordinateurs de bureau et portables'),
        ('Périphériques', 'Souris, claviers, écrans'),
        ('Réseau', 'Routeurs, switches, câbles'),
        ('Stockage', 'Disques durs, SSD, clés USB'),
        ('Logiciels', 'Licences et logiciels'),
        ('Accessoires', 'Autres accessoires informatiques')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)', default_categories)
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Main dashboard"""
    conn = get_db_connection()
    
    # Get materials with low stock
    low_stock = conn.execute('''
        SELECT * FROM materials 
        WHERE quantity <= min_stock 
        ORDER BY quantity ASC
    ''').fetchall()
    
    # Get recent transactions
    recent_transactions = conn.execute('''
        SELECT t.*, m.name as material_name 
        FROM transactions t 
        JOIN materials m ON t.material_id = m.id 
        ORDER BY t.created_at DESC 
        LIMIT 10
    ''').fetchall()
    
    # Get total materials count
    total_materials = conn.execute('SELECT COUNT(*) as count FROM materials').fetchone()['count']
    
    # Get total value
    total_value = conn.execute('SELECT SUM(price * quantity) as total FROM materials').fetchone()['total'] or 0
    
    conn.close()
    
    return render_template('index.html', 
                         low_stock=low_stock,
                         recent_transactions=recent_transactions,
                         total_materials=total_materials,
                         total_value=total_value)

@app.route('/materials')
def materials():
    """Materials management page"""
    conn = get_db_connection()
    materials = conn.execute('''
        SELECT m.*, c.name as category_name 
        FROM materials m 
        LEFT JOIN categories c ON m.category = c.name 
        ORDER BY m.name
    ''').fetchall()
    conn.close()
    return render_template('materials.html', materials=materials)

@app.route('/add_material', methods=['GET', 'POST'])
def add_material():
    """Add new material"""
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        brand = request.form['brand']
        model = request.form['model']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        min_stock = int(request.form['min_stock'])
        supplier = request.form['supplier']
        description = request.form['description']
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO materials (name, category, brand, model, price, quantity, min_stock, supplier, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, category, brand, model, price, quantity, min_stock, supplier, description))
        conn.commit()
        conn.close()
        
        flash('Matériel ajouté avec succès!', 'success')
        return redirect(url_for('materials'))
    
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories ORDER BY name').fetchall()
    conn.close()
    return render_template('add_material.html', categories=categories)

@app.route('/edit_material/<int:id>', methods=['GET', 'POST'])
def edit_material(id):
    """Edit material"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        brand = request.form['brand']
        model = request.form['model']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        min_stock = int(request.form['min_stock'])
        supplier = request.form['supplier']
        description = request.form['description']
        
        conn.execute('''
            UPDATE materials 
            SET name=?, category=?, brand=?, model=?, price=?, quantity=?, min_stock=?, supplier=?, description=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        ''', (name, category, brand, model, price, quantity, min_stock, supplier, description, id))
        conn.commit()
        conn.close()
        
        flash('Matériel modifié avec succès!', 'success')
        return redirect(url_for('materials'))
    
    material = conn.execute('SELECT * FROM materials WHERE id = ?', (id,)).fetchone()
    categories = conn.execute('SELECT * FROM categories ORDER BY name').fetchall()
    conn.close()
    
    if material is None:
        flash('Matériel non trouvé!', 'error')
        return redirect(url_for('materials'))
    
    return render_template('edit_material.html', material=material, categories=categories)

@app.route('/delete_material/<int:id>')
def delete_material(id):
    """Delete material"""
    conn = get_db_connection()
    conn.execute('DELETE FROM materials WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Matériel supprimé avec succès!', 'success')
    return redirect(url_for('materials'))

@app.route('/transaction/<int:id>', methods=['GET', 'POST'])
def transaction(id):
    """Handle stock transactions"""
    conn = get_db_connection()
    material = conn.execute('SELECT * FROM materials WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        transaction_type = request.form['type']
        quantity = int(request.form['quantity'])
        reason = request.form['reason']
        user = request.form['user']
        
        if transaction_type == 'in':
            new_quantity = material['quantity'] + quantity
        else:  # out
            if material['quantity'] < quantity:
                flash('Stock insuffisant!', 'error')
                return redirect(url_for('transaction', id=id))
            new_quantity = material['quantity'] - quantity
        
        # Update material quantity
        conn.execute('UPDATE materials SET quantity = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', 
                    (new_quantity, id))
        
        # Add transaction record
        conn.execute('''
            INSERT INTO transactions (material_id, transaction_type, quantity, reason, user)
            VALUES (?, ?, ?, ?, ?)
        ''', (id, transaction_type, quantity, reason, user))
        
        conn.commit()
        conn.close()
        
        flash('Transaction enregistrée avec succès!', 'success')
        return redirect(url_for('materials'))
    
    conn.close()
    return render_template('transaction.html', material=material)

@app.route('/reports')
def reports():
    """Reports page"""
    conn = get_db_connection()
    
    # Stock report
    stock_report = conn.execute('''
        SELECT category, COUNT(*) as count, SUM(quantity) as total_quantity, SUM(price * quantity) as total_value
        FROM materials 
        GROUP BY category 
        ORDER BY total_value DESC
    ''').fetchall()
    
    # Low stock report
    low_stock_report = conn.execute('''
        SELECT * FROM materials 
        WHERE quantity <= min_stock 
        ORDER BY (quantity - min_stock) ASC
    ''').fetchall()
    
    conn.close()
    return render_template('reports.html', stock_report=stock_report, low_stock_report=low_stock_report)

# API endpoints
@app.route('/api/materials')
def api_materials():
    """API endpoint to get all materials"""
    conn = get_db_connection()
    materials = conn.execute('SELECT * FROM materials ORDER BY name').fetchall()
    conn.close()
    
    return jsonify([dict(material) for material in materials])

@app.route('/api/materials/<int:id>')
def api_material(id):
    """API endpoint to get specific material"""
    conn = get_db_connection()
    material = conn.execute('SELECT * FROM materials WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if material is None:
        return jsonify({'error': 'Material not found'}), 404
    
    return jsonify(dict(material))

@app.route('/api/transactions')
def api_transactions():
    """API endpoint to get all transactions"""
    conn = get_db_connection()
    transactions = conn.execute('''
        SELECT t.*, m.name as material_name 
        FROM transactions t 
        JOIN materials m ON t.material_id = m.id 
        ORDER BY t.created_at DESC
    ''').fetchall()
    conn.close()
    
    return jsonify([dict(transaction) for transaction in transactions])

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
