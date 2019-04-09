import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class DB:
    def __init__(self):
        conn = sqlite3.connect('static\\bd\\BD.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class UserModel:
    def __init__(self, connection):
        self.connection = connection

    def insert(self, user_name, password, permission):
        cursor = self.connection.cursor()
        password_hash = generate_password_hash(password)
        cursor.execute('''INSERT INTO users
                          (user_name, password_hash, permission)
                          VALUES (?,?,?)''', (user_name, password_hash, permission))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, user_name, password=None):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?", (user_name,))
        row = cursor.fetchone()
        if row:
            if password:
                if check_password_hash(row[2], password):
                    return [True, row[0], row[3]]
                else:
                    return [False]
            else:
                return True if row else False
        else:
            return [False]

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128),
                             permission VARCHAR(16)
                             )''')
        cursor.close()
        self.connection.commit()


class NewsModel:
    def __init__(self, connection):
        self.connection = connection

    def insert(self,  user_id, title, content, image, project):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO news
                          (user_id, title, content, image, project)
                          VALUES (?,?,?,?,?)''', (str(user_id), title, content, str(image), project))
        cursor.close()
        self.connection.commit()

    def get(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE id = ?", (str(news_id),))
        row = cursor.fetchone()
        return row

    def get_all(self, project=None):
        cursor = self.connection.cursor()
        if project:
            cursor.execute("SELECT * FROM news WHERE project = ?", (str(project),))
        else:
            cursor.execute("SELECT * FROM news")
        rows = sorted(cursor.fetchall(), reverse=True)
        return rows

    def delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM news WHERE id = ?''', (str(news_id),))
        cursor.close()
        self.connection.commit()

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             user_id INTEGER, 
                             title VARCHAR(100),
                             content VARCHAR(1000),
                             image VARCHAR(1000),
                             project VARCHAR(100)
                             )''')
        cursor.close()
        self.connection.commit()
