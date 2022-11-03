import sys
import apsw
from apsw import Error

conn = None


def setup():
    try:
        conn = apsw.Connection('./tiny.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS messages (
                id integer PRIMARY KEY, 
                sender integer NOT NULL,
                recipient integer NOT NULL,
                replyto integer,
                message TEXT NOT NULL,
                CONSTRAINT fk_sender
                    FOREIGN KEY(sender) REFERENCES users(id),
                CONSTRAINT fk_recipient
                    FOREIGN KEY(recipient) REFERENCES users(id),
                CONSTRAINT fk_replyto
                    FOREIGN KEY(replyto) REFERENCES messages(id));''')
        c.execute('''CREATE TABLE IF NOT EXISTS announcements (
                id integer PRIMARY KEY, 
                author TEXT NOT NULL,
                text TEXT NOT NULL);''')
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                id  integer PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                salt TEXT NOT NULL,
                password TEXT NOT NULL);''')
        conn.close()
    except Error as e:
        print(e)
        sys.exit(1)


def get_user(username):
    try:
        conn = apsw.Connection('./tiny.db')
        c = conn.cursor()
        c = c.execute('''SELECT * FROM users WHERE username = ?''', (username,))
        res = c.fetchone()
        conn.close()
        return res
    except Error as e:
        print(e)


def add_user(username, salt, password):
    try:
        conn = apsw.Connection('./tiny.db')
        c = conn.cursor()
        c.execute('''INSERT INTO users (username, salt, password) VALUES (?,?,?)''', (username, salt, password))
        conn.close()
    except Error as e:
        print(e)


def get_user_by_id(id):
    try:
        conn = apsw.Connection('./tiny.db')
        c = conn.cursor()
        c = c.execute('''SELECT * FROM users WHERE id = ?''', (id,))
        res = c.fetchone()
        conn.close()
        return res
    except Error as e:
        print(e)


def get_user_by_name(username):
    try:
        conn = apsw.Connection('./tiny.db')
        c = conn.cursor()
        c = c.execute('''SELECT * FROM users WHERE username = ?''', (username,))
        res = c.fetchone()
        conn.close()
        return res
    except Error as e:
        print(e)


def add_message(sender, message, recipient):
    try:
        conn = apsw.Connection('./tiny.db')
        c = conn.cursor()
        c.execute('''INSERT INTO messages (sender, message, recipient) VALUES (?,?,?)''',
                  (sender, message, recipient))
        conn.close()
    except Error as e:
        print(e)


def get_message_by_id(id, user_id):
    try:
        conn = apsw.Connection('./tiny.db')
        c = conn.cursor()
        c = c.execute('''SELECT * FROM messages WHERE id = ? AND (? = sender OR ? = recipient)''',
                      (id, user_id, user_id))
        res = c.fetchone()
        conn.close()
        return res
    except Error as e:
        print(e)


def get_messages(user_id):
    try:
        conn = apsw.Connection('./tiny.db')
        c = conn.cursor()
        c = c.execute('''SELECT * FROM messages WHERE (? = sender OR ? = recipient)''',
                      (user_id, user_id))
        res = c.fetchall()
        conn.close()
        return res
    except Error as e:
        print(e)


def search_messages(query, user_id):
    try:
        conn = apsw.Connection('./tiny.db')
        c = conn.cursor()
        c = c.execute('''SELECT * FROM messages WHERE message GLOB ? AND (? = sender OR ? = recipient)''',
                         (query, user_id, user_id))
        res = c.fetchall()
        conn.close()
        return res
    except Error as e:
        print(e)


def get_announcements():
    try:
        conn = apsw.Connection('./tiny.db')
        c = conn.cursor()
        c = c.execute('''SELECT * FROM announcements''')
        res = c.fetchall()
        conn.close()
        return res
    except Error as e:
        print(e)

