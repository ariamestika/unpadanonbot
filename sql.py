import sqlite3

def create_users_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # create table to store user information
    c.execute('''CREATE TABLE users
                 (id INTEGER PRIMARY KEY, gender text, uni text, partnergender text, partneruni text)''')

    # create table to store user's chat history
    c.execute('''CREATE TABLE chats
                 (id INTEGER PRIMARY KEY, user1 INTEGER, user2 INTEGER, FOREIGN KEY (user1) REFERENCES users(id), FOREIGN KEY (user2) REFERENCES users(id))''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_users_db()
