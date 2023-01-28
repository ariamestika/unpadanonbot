import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot("5436395817:AAFngaB7h9MsHc1fA8et4sFOWVEPJ04WkOI")

# Create users.db if it doesn't exist
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    gender TEXT,
                    partner_gender TEXT,
                    uni TEXT,
                    partner_uni TEXT
                )""")
conn.commit()

# Gender command
@bot.message_handler(commands=['gender'])
def gender(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row("/male", "/female", "/others")
    bot.send_message(message.chat.id, "Please choose your gender:", reply_markup=markup)

# Partner gender command
@bot.message_handler(commands=['partnergender'])
def partner_gender(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row("/male", "/female", "/others")
    bot.send_message(message.chat.id, "Please choose the partner's gender you want to search for:", reply_markup=markup)

# Uni command
@bot.message_handler(commands=['uni'])
def uni(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row("/unpad", "/non-unpad")
    bot.send_message(message.chat.id, "Please choose your university:", reply_markup=markup)

# Partner uni command
@bot.message_handler(commands=['partneruni'])
def partner_uni(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row("/unpad", "/non-unpad")
    bot.send_message(message.chat.id, "Please choose the partner's university you want to search for:", reply_markup=markup)

# Report command
@bot.message_handler(commands=['report'])
def report(message):
    bot.send_message(message.chat.id, "Please provide details of the report:")

# Search command
@bot.message_handler(commands=['search'])
def search(message):
    # Get user's preferences
    cursor.execute("SELECT * FROM users WHERE id=?", (message.from_user.id,))
    user_pref = cursor.fetchone()
    if user_pref is None:
        bot.send_message(message.chat.id, "Please set your preferences first using /gender, /partnergender, /uni, and /partneruni.")
        return

    # Search for partners with matching preferences
    cursor.execute("SELECT id FROM users WHERE gender=? AND partner_gender=? AND uni=? AND partner_uni=?", (user_pref[1], user_pref[2], user_pref[3], user_pref[4]))
    partner_id = cursor.fetchone()
    if partner_id is None:
        bot.send_message(message.chat.id, "No partners with matching preferences found.")
        return
        
    # Connect user with partner
    bot.send_message(partner_id[0], "You have been connected with a new partner.")
    bot.send_message(message.chat.id, "You have been connected with a new partner.")

#Stop command
@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(message.chat.id, "Current chat has been stopped.")

#Profile command
@bot.message_handler(commands=['profile'])
def profile(message):
    bot.send_message(message.chat.id, "Please use the /gender, /partnergender, /uni, and /partneruni commands to change your preferences.")

#Contact command
@bot.message_handler(commands=['contact'])
def contact(message):
    bot.send_message(message.chat.id, "For any questions or concerns, please contact the administrator at admin@example.com.")

bot.polling()
