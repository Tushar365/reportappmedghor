"""Database operations for Medghor Focus Item PDF Generator"""
import sqlite3
import json
from datetime import datetime
import hashlib

def init_db():
    """Initialize main application database tables"""
    conn = sqlite3.connect('medghor_reports.db')
    c = conn.cursor()
    
    # Create reports table
    c.execute('''CREATE TABLE IF NOT EXISTS reports
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  start_date TEXT,
                  end_date TEXT,
                  brand_name TEXT,
                  products TEXT,
                  user_id INTEGER DEFAULT 1,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create products table
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  product_name TEXT UNIQUE,
                  last_rate TEXT,
                  usage_count INTEGER DEFAULT 1,
                  last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

def init_auth_db():
    """Initialize authentication tables"""
    conn = sqlite3.connect('medghor_reports.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  full_name TEXT,
                  role TEXT DEFAULT 'viewer',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  last_login TIMESTAMP,
                  is_active INTEGER DEFAULT 1,
                  failed_login_attempts INTEGER DEFAULT 0)''')
    
    # User sessions table
    c.execute('''CREATE TABLE IF NOT EXISTS user_sessions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  session_token TEXT UNIQUE,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  expires_at TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

def save_report(start_date, end_date, brand_name, products, user_id=1):
    """Save report to database"""
    conn = sqlite3.connect('medghor_reports.db')
    c = conn.cursor()
    
    products_json = json.dumps(products)
    c.execute('''INSERT INTO reports (start_date, end_date, brand_name, products, user_id)
                 VALUES (?, ?, ?, ?, ?)''',
              (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), 
               brand_name, products_json, user_id))
    
    # Update products usage
    for product in products:
        c.execute('''INSERT INTO products (product_name, last_rate, usage_count, last_used)
                     VALUES (?, ?, 1, CURRENT_TIMESTAMP)
                     ON CONFLICT(product_name) DO UPDATE SET
                     last_rate = ?,
                     usage_count = usage_count + 1,
                     last_used = CURRENT_TIMESTAMP''',
                  (product['name'], product['rate'], product['rate']))
    
    conn.commit()
    conn.close()

def get_all_reports(user_id=None):
    """Retrieve all reports from database"""
    conn = sqlite3.connect('medghor_reports.db')
    c = conn.cursor()
    
    if user_id:
        c.execute('SELECT * FROM reports WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    else:
        c.execute('SELECT * FROM reports ORDER BY created_at DESC')
    
    reports = c.fetchall()
    conn.close()
    return reports

def get_popular_products(limit=20):
    """Get most frequently used products"""
    conn = sqlite3.connect('medghor_reports.db')
    c = conn.cursor()
    c.execute('SELECT product_name, last_rate, usage_count FROM products ORDER BY usage_count DESC LIMIT ?', (limit,))
    products = c.fetchall()
    conn.close()
    return products

def delete_report(report_id):
    """Delete a report by ID"""
    conn = sqlite3.connect('medghor_reports.db')
    c = conn.cursor()
    c.execute('DELETE FROM reports WHERE id = ?', (report_id,))
    conn.commit()
    conn.close()

def load_report(report_id):
    """Load a specific report by ID"""
    conn = sqlite3.connect('medghor_reports.db')
    c = conn.cursor()
    c.execute('SELECT start_date, end_date, brand_name, products FROM reports WHERE id = ?', (report_id,))
    report = c.fetchone()
    conn.close()
    return report

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password, full_name, role='viewer'):
    """Create a new user"""
    conn = sqlite3.connect('medghor_reports.db')
    c = conn.cursor()
    
    password_hash = hash_password(password)
    
    try:
        c.execute('''INSERT INTO users (username, email, password_hash, full_name, role)
                     VALUES (?, ?, ?, ?, ?)''',
                  (username, email, password_hash, full_name, role))
        conn.commit()
        return True, "User created successfully"
    except sqlite3.IntegrityError:
        return False, "Username or email already exists"
    finally:
        conn.close()

def authenticate_user(username, password):
    """Authenticate user credentials"""
    conn = sqlite3.connect('medghor_reports.db')
    c = conn.cursor()
    
    password_hash = hash_password(password)
    
    c.execute('''SELECT id, username, email, full_name, role, is_active, failed_login_attempts
                 FROM users WHERE username = ? AND password_hash = ?''',
              (username, password_hash))
    
    user = c.fetchone()
    
    if user:
        user_id = user[0]
        # Reset failed attempts
        c.execute('UPDATE users SET failed_login_attempts = 0, last_login = CURRENT_TIMESTAMP WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        return True, {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'full_name': user[3],
            'role': user[4],
            'is_active': user[5]
        }
    else:
        # Increment failed attempts
        c.execute('UPDATE users SET failed_login_attempts = failed_login_attempts + 1 WHERE username = ?', (username,))
        conn.commit()
        conn.close()
        return False, None
