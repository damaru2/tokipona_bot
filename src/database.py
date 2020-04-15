import sqlite3
import os.path
import threading
import functools
import traceback


def lock(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        with TokiPonaDB.lock_db:
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                print(traceback.format_exc())
                self.conn.commit()
                self.conn.close()
    return wrapper


class TokiPonaDB:

    lock_db = threading.Lock()

    def __init__(self, db_folder='data'):
        db_name = "{}/users.db".format(db_folder)
        create_tables = not os.path.isfile(db_name)
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        if create_tables:
            self.__create_tables()

    def __create_tables(self):
        # id_selected_game is the id_group of the game selected by the user
        self.conn.execute(
            '''CREATE TABLE users (
                id_chat             INTEGER PRIMARY KEY,
                font_type           INTEGER DEFAULT 1,
                font_color          STRING DEFAULT "000000",
                background_color    STRING DEFAULT "FFFFFF")
                ''')
        self.conn.commit()

    @lock
    def get_data(self, id_chat):
        query = '''SELECT font_type, font_color, background_color FROM users
                    WHERE id_chat = ?'''
        ret = self.cur.execute(query, (id_chat,)).fetchone()
        if not ret:
            return None
        else:
            return (ret[0], ret[1], ret[2])

    @lock
    def update_font_type(self, id_chat, font_type):
        update_query = '''UPDATE users
                          SET font_type = ?
                          WHERE id_chat = ?'''
        self.conn.execute(update_query, (font_type, id_chat))
        self.conn.commit()

    @lock
    def update_font_color(self, id_chat, font_color):
        update_query = '''UPDATE users
                          SET font_color = ?
                          WHERE id_chat = ?'''
        self.conn.execute(update_query, (font_color, id_chat))
        self.conn.commit()

    @lock
    def update_background_color(self, id_chat, background_color):
        update_query = '''UPDATE users
                          SET background_color = ?
                          WHERE id_chat = ?'''
        self.conn.execute(update_query, (background_color, id_chat))
        self.conn.commit()

    @lock
    def insert_new_user(self, id_chat):
        insert_new_user = '''INSERT INTO users (id_chat) VALUES (?)'''
        self.conn.execute(insert_new_user, (id_chat,))
        self.conn.commit()


if __name__ == "__main__":
    pass
    #db = TokiPonaDB()
    #db.conn.commit()
