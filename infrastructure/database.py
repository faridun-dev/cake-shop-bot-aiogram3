import sqlite3


class BotDatabase:
    def __init__(self):
        # Устанавливаем соединение с базой данных (если файл не существует — он будет создан)
        self.connection = sqlite3.connect("bot_db.db")
        self.cursor = self.connection.cursor()

        # Создаём таблицу Orders, если она ещё не существует
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Уникальный ID (автоматически увеличивается)
            order_id INTEGER UNIQUE,                -- Уникальный ID заказа
            user TEXT NOT NULL,                     -- Имя пользователя или ID
            name TEXT NOT NULL,                     -- Название товара
            amount INTEGER,                         -- Количество
            price TEXT,                             -- Цена (можно заменить на REAL, если нужно число)
            status BOOLEAN DEFAULT 0                -- Статус (оплачен или нет), по умолчанию False (0)
        )
        """)

        self.connection.commit()

    def add_order(self, order_info: tuple):
        """
        Добавляет новый заказ в базу данных.
        Параметр order_info — это кортеж с данными: (order_id, user, name, amount, price, status)
        """
        try:
            self.cursor.execute(
                "INSERT INTO Orders (order_id, user, name, amount, price, status) VALUES (?, ?, ?, ?, ?, ?)",
                order_info,
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            # Ошибка возникает, если order_id уже существует
            raise ValueError("Дубликат order_id. Попробуйте другой ID.")
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")

    def update_order_status(self, order_id: int, status: bool):
        """
        Обновляет статус заказа (например, оплачен/не оплачен)
        """
        try:
            self.cursor.execute(
                "UPDATE Orders SET status = ? WHERE order_id = ?",
                (status, order_id),
            )
            self.connection.commit()

            if self.cursor.rowcount == 0:
                # Если не обновилось ни одной строки — заказ с таким ID не найден
                raise ValueError("Заказ с таким ID не найден.")
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")

    def close(self):
        # Закрываем соединение с базой данных
        self.connection.close()
