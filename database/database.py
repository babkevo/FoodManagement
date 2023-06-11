import sqlite3


def create_tables():
    conn = sqlite3.connect('food_items.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS food_items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 expiration_date DATE NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 password TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS suggested_items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 item_name TEXT NOT NULL,
                 quantity INTEGER DEFAULT 0)''')

    conn.commit()
    conn.close()


def insert_food_item(name, expiration_date):
    conn = sqlite3.connect('food_items.db')
    c = conn.cursor()

    c.execute("INSERT INTO food_items (name, expiration_date) VALUES (?, ?)",
        (name, expiration_date))

    conn.commit()
    conn.close()


def get_food_items():
    conn = sqlite3.connect('food_items.db')
    c = conn.cursor()

    c.execute("SELECT * FROM food_items")
    items = c.fetchall()

    conn.close()

    return items


def get_expired_items():
    conn = sqlite3.connect('food_items.db')
    c = conn.cursor()

    c.execute("SELECT * FROM food_items WHERE expiration_date < DATE('now')")
    expired_items = c.fetchall()

    print(expired_items)  # Add this line

    conn.close()

    return expired_items


def get_suggested_items():
    expired_items = get_expired_items()
    print(expired_items)  # we print and see if it works
    suggested_items = {}

    for item in expired_items:
        name = item[1]  # Assuming the name is stored in the second column
        if name in suggested_items:
            suggested_items[name] += 1
        else:
            suggested_items[name] = 1

    return suggested_items


def setup_suggested_items():
    conn = sqlite3.connect('food_items.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS suggested_items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 item_name TEXT NOT NULL,
                 quantity INTEGER DEFAULT 0)''')

    conn.commit()
    conn.close()


# Call create_tables() to create the necessary tables
create_tables()
