import pyTelegramBotAPI as telebot
import sqlite3

bot = telebot.TeleBot("5436395817:AAFngaB7h9MsHc1fA8et4sFOWVEPJ04WkOI")

# Connect to the database
conn = sqlite3.connect("database.db")
c = conn.cursor()

# Create tables for the database if they don't already exist
c.execute('''CREATE TABLE IF NOT EXISTS users (
                chat_id INTEGER PRIMARY KEY,
                gender TEXT,
                partner_gender TEXT,
                uni TEXT,
                partner_uni TEXT)''')

# Handle the /start command
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Welcome to the anonymous chat bot! Type /help to see a list of available commands.")

# Handle the /gender command
@bot.message_handler(commands=["gender"])
def gender(message):
    c.execute("INSERT INTO users (chat_id) VALUES (?)", (message.chat.id,))
    bot.reply_to(message, "Please choose your gender: /male, /female, or /others")

# Handle the /partnergender command
@bot.message_handler(commands=["partnergender"])
def partner_gender(message):
    c.execute("UPDATE users SET partner_gender = ? WHERE chat_id = ?", (message.text, message.chat.id))
    bot.reply_to(message, "Please choose the gender of your desired partner: /male, /female, or /others")

# Handle the /uni command
@bot.message_handler(commands=["uni"])
def uni(message):
    c.execute("UPDATE users SET uni = ? WHERE chat_id = ?", (message.text, message.chat.id))
    bot.reply_to(message, "Please choose your university: /unpad, or /non-unpad")

# Handle the /partneruni command
@bot.message_handler(commands=["partneruni"])
def partner_uni(message):
    c.execute("UPDATE users SET partner_uni = ? WHERE chat_id = ?", (message.text, message.chat.id))
    bot.reply_to(message, "Please choose the university of your desired partner: /unpad, or /non-unpad")

# Handle the /report command
@bot.message_handler(commands=["report"])
def report(message):
    # Code to handle reporting here
    bot.reply_to(message, "Thank you for your report. It has been submitted for review.")

# Handle the /stop command
@bot.message_handler(commands=["stop"])
def stop(message):
    # Code to handle stopping the current chat here
    bot.reply_to(message, "You have stopped the current chat.")

# Handle the /profile command
@bot.message_handler(commands=["profile"])
def profile(message):
    # Code to handle updating profile information here
    bot.reply_to(message, "Your profile information has been updated.")


# Handle the /contact command
@bot.message_handler(commands=["contact"])
def contact(message):
    bot.reply_to(message, "If you need to contact an administrator, please send an email to admin@example.com")

# Handle the /search command
@bot.message_handler(commands=["search"])
def search(message):
    # Code to search for partners based on user preferences and connect them
    bot.reply_to(message, "Searching for partners...")
    # Connect users whose preferences match
    c.execute("SELECT chat_id FROM users WHERE gender = (SELECT partner_gender FROM users WHERE chat_id = ?) AND uni = (SELECT partner_uni FROM users WHERE chat_id = ?)", (message.chat.id, message.chat.id))
    match = c.fetchone()
    if match:
        bot.send_message(match[0], "You have been connected with a new partner. Say hi!")
        bot.send_message(message.chat.id, "You have been connected with a new partner. Say hi!")
    else:
        bot.reply_to(message, "No match found.")

# Handle all other messages
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    bot.reply_to(message, "Sorry, I didn't understand that. Type /help to see a list of available commands.")

# Commit changes to the database and close the connection
conn.commit()
conn.close()

# Start the bot
bot.polling()
