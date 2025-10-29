#!/usr/bin/env python3
"""
Test script for the Inventory Management System
Tests database initialization and basic functionality
"""

import sqlite3
import os
import sys

def test_database_creation():
    """Test if database can be created and initialized"""
    print("Testing database creation...")
    
    # Remove existing database if it exists
    if os.path.exists('inventory.db'):
        os.remove('inventory.db')
        print("Removed existing database")
    
    # Test database creation
    try:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        
        # Test basic table creation
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0
            )
        ''')
        
        # Test data insertion
        cursor.execute('''
            INSERT INTO test_materials (name, category, price, quantity)
            VALUES (?, ?, ?, ?)
        ''', ('Test Material', 'Test Category', 99.99, 10))
        
        # Test data retrieval
        cursor.execute('SELECT * FROM test_materials WHERE name = ?', ('Test Material',))
        result = cursor.fetchone()
        
        if result:
            print("✓ Database creation and basic operations successful")
            print(f"✓ Test material: {result[1]} - {result[3]}€ - Qty: {result[4]}")
        else:
            print("✗ Database test failed - no data retrieved")
            return False
            
        conn.commit()
        conn.close()
        
        # Clean up test database
        os.remove('inventory.db')
        print("✓ Test database cleaned up")
        
        return True
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_flask_imports():
    """Test if Flask and required modules can be imported"""
    print("\nTesting Flask imports...")
    
    try:
        import flask
        print(f"✓ Flask {flask.__version__} imported successfully")
        
        import sqlite3
        print("✓ sqlite3 imported successfully")
        
        import os
        print("✓ os imported successfully")
        
        from datetime import datetime
        print("✓ datetime imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'app.PY',
        'DATA.SQL',
        'requirements.txt',
        'static/style.css',
        'static/script.js',
        'templates/base.html',
        'templates/index.html',
        'templates/materials.html',
        'templates/add_material.html',
        'templates/edit_material.html',
        'templates/transaction.html',
        'templates/reports.html'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("=" * 50)
    print("INVENTORY MANAGEMENT SYSTEM - TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Flask Imports", test_flask_imports),
        ("Database Creation", test_database_creation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        if test_func():
            passed += 1
        else:
            print(f"✗ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready to use.")
        print("\nTo start the application:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the application: python app.PY")
        print("3. Open browser: http://localhost:5000")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
