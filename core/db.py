import sqlite3


class BotDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        user = result.fetchone()
        print(f"user_exists check for user_id {user_id}: {user}")
        return user is not None

    def get_user_id(self, user_id):
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'user_id' = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        self.cursor.execute("INSERT OR IGNORE INTO 'users' ('user_id') VALUES (?)", (user_id,))
        self.conn.commit()
        return self

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        self.conn.commit()
        return self

    def id_for_print(self):
        self.cursor.execute("SELECT user_id FROM users")
        user_ids = self.cursor.fetchall()
        return [user_id[0] for user_id in user_ids]


    def close(self):
        self.conn.close()
