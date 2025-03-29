import sqlite3

class BotDatabase:
    def __init__(self):
        self.connection = sqlite3.connect('bot_db.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER UNIQUE,
            user TEXT NOT NULL,
            name TEXT NOT NULL,
            amount INTEGER,
            price TEXT,
            status BOOLEAN DEFAULT 0
        )
        ''')

        self.connection.commit()
    
    def add_order(self, order_info: tuple):
        try:
            self.cursor.execute(
                'INSERT INTO Orders (order_id, user, name, amount, price, status) VALUES (?, ?, ?, ?, ?, ?)',
                order_info
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Duplicate order_id, try again with a new one.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def update_order_status(self, order_id: int, status: bool):
        try:
            self.cursor.execute(
                'UPDATE Orders SET status = ? WHERE order_id = ?',
                (status, order_id)
            )
            self.connection.commit()

            if self.cursor.rowcount == 0:
                raise ValueError("Order ID not found.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def close(self):
        self.connection.close()
