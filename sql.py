import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create the users table
c.execute('''
CREATE TABLE users (
    chat_id INTEGER PRIMARY KEY,
    gender TEXT,
    uni TEXT,
    partnergender TEXT,
    partneruni TEXT
);
''')

# Create the chats table
c.execute('''
CREATE TABLE chats (
    user1 INTEGER,
    user2 INTEGER
);
''')


# Commit the changes
conn.commit()

# Close the connection
conn.close()
