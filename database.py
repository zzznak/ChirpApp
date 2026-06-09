import sqlite3
import hashlib
from datetime import datetime
from security import generate_user_keys

def get_db():
    return sqlite3.connect("messenger.db", check_same_thread=False)

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Таблица пользователей с уникальным username и public_key
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, 
                       email TEXT UNIQUE, 
                       password TEXT, 
                       username TEXT UNIQUE, 
                       public_key TEXT,
                       avatar TEXT,
                       status TEXT DEFAULT "Привет!",
                       is_online BOOLEAN DEFAULT 0)''')
    
    # Таблица сообщений
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages 
                      (id INTEGER PRIMARY KEY, 
                       sender TEXT, 
                       receiver TEXT, 
                       content TEXT, 
                       is_encrypted BOOLEAN DEFAULT 1,
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                       is_read BOOLEAN DEFAULT 0)''')
    
    # Таблица групп
    cursor.execute('''CREATE TABLE IF NOT EXISTS groups
                      (id INTEGER PRIMARY KEY,
                       group_name TEXT UNIQUE,
                       creator TEXT,
                       avatar TEXT,
                       created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Таблица членов групп
    cursor.execute('''CREATE TABLE IF NOT EXISTS group_members
                      (id INTEGER PRIMARY KEY,
                       group_id INTEGER,
                       username TEXT,
                       joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY(group_id) REFERENCES groups(id))''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(email, password, username):
    try:
        conn = get_db()
        cursor = conn.cursor()
        pub_key = generate_user_keys()  # Генерируем ключ при регистрации
        # Используем первую букву юзернейма как аватар
        avatar = username[0].upper()
        cursor.execute("""INSERT INTO users (email, password, username, public_key, avatar) 
                       VALUES (?, ?, ?, ?, ?)""", 
                       (email, hash_password(password), username, pub_key, avatar))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Email или Username уже заняты
    finally:
        conn.close()

def check_login(email, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE email=? AND password=?", 
                   (email, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def get_all_users(current_email):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE email != ?", (current_email,))
    data = cursor.fetchall()
    conn.close()
    return [item[0] for item in data]

def find_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, public_key, avatar, is_online FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def user_exists(email, username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE email=? OR username=?", (email, username))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def save_message(sender, receiver, content, is_encrypted=True):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO messages (sender, receiver, content, is_encrypted) 
                   VALUES (?, ?, ?, ?)""", 
                   (sender, receiver, content, is_encrypted))
    conn.commit()
    conn.close()

def get_chat_history(user1, user2, limit=50):
    conn = get_db()
    cursor = conn.cursor()
    # Получаем историю переписки между двумя людьми
    cursor.execute("""SELECT sender, content, timestamp, is_read FROM messages 
                   WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?) 
                   ORDER BY timestamp DESC
                   LIMIT ?""", (user1, user2, user2, user1, limit))
    messages = cursor.fetchall()
    conn.close()
    return list(reversed(messages))  # Развернуть для хронологического порядка

def set_user_online(username, is_online):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_online=? WHERE username=?", (is_online, username))
    conn.commit()
    conn.close()

def get_user_status(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT is_online FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else False

# Инициализируем БД при запуске файла
if __name__ == "__main__":
    init_db()
    print("✅ База данных инициализирована!")
