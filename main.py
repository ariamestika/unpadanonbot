import telebot
import pytz
import os
import time
from telebot import types
import sqlite3
conn = sqlite3.connect('users.db')
c = conn.cursor()


bot = telebot.TeleBot(os.environ.get('5436395817:AAFngaB7h9MsHc1fA8et4sFOWVEPJ04WkOI'))

# function for /gender command
@bot.message_handler(commands=['gender'])
def choose_gender(message):
    msg = bot.reply_to(message, "Please choose your gender: /male, /female, /others")
    bot.register_next_step_handler(msg, process_gender_step)

def process_gender_step(message):
    chat_id = message.chat.id
    if message.text == '/male':
        bot.send_message(chat_id, "Your gender is set as Male")
        # save gender to database
    elif message.text == '/female':
        bot.send_message(chat_id, "Your gender is set as Female")
        # save gender to database
    elif message.text == '/others':
        bot.send_message(chat_id, "Your gender is set as Others")
        # save gender to database
    else:
        bot.send_message(chat_id, "Invalid input. Please choose /male, /female, or /others")
        choose_gender(message)

# function for /partnergender command
@bot.message_handler(commands=['partnergender'])
def choose_partner_gender(message):
    msg = bot.reply_to(message, "Please choose your partner's gender: /male, /female, /others")
    bot.register_next_step_handler(msg, process_partner_gender_step)

def process_partner_gender_step(message):
    chat_id = message.chat.id
    if message.text == '/male':
        bot.send_message(chat_id, "Your partner's gender is set as Male")
        # save partner gender to database
    elif message.text == '/female':
        bot.send_message(chat_id, "Your partner's gender is set as Female")
        # save partner gender to database
    elif message.text == '/others':
        bot.send_message(chat_id, "Your partner's gender is set as Others")
        # save partner gender to database
    else:
        bot.send_message(chat_id, "Invalid input. Please choose /male, /female, or /others")
        choose_partner_gender(message)

# function for /uni command
@bot.message_handler(commands=['uni'])
def choose_uni(message):
    msg = bot.reply_to(message, "Please choose your university: /unpad, /non-unpad")
    bot.register_next_step_handler(msg, process_uni_step)

def process_uni_step(message):
    chat_id = message.chat.id
    if message.text == '/unpad':
        bot.send_message(chat_id, "Your university is set as UNPAD")
        # save uni to database
    elif message.text == '/non-unpad':
        bot.send_message(chat_id, "Your university is set as Non-UNPAD")
        # save uni to database
    else:
        bot.send_message(chat_id, "Invalid input. Please choose /unpad or /non-unpad")
        choose_uni(message)

# function for /partneruni command
@bot.message_handler(commands=['partneruni'])
def choose_partner_uni(message):
    msg = bot.reply_to(message, "Please choose your partner's university: /unpad, /non-unpad")
    bot.register_next_step_handler(msg, process_partner_uni_step)

def process_partner_uni_step(message):
    chat_id = message.chat.id
    if message.text == '/unpad':
        bot.send_message(chat_id, "Your partner's university is set as UNPAD")
        # save partner uni to database
    elif message.text == '/non-unpad':
        bot.send_message(chat_id, "Your partner's university is set as Non-UNPAD")
        # save partner uni to database
    else:
        bot.send_message(chat_id, "Invalid input. Please choose /unpad or /non-unpad")
        choose_partner_uni(message)

# Handle the /search command
@bot.message_handler(commands=['search'])
def search(message):
    # Get the user's chat ID
    chat_id = message.chat.id

    # Check if the user has set their gender, uni, partner gender and partner uni preferences
    c.execute('SELECT * FROM users WHERE id=?', (chat_id,))
    user = c.fetchone()
    if user is None or user[1] is None or user[2] is None or user[3] is None or user[4] is None:
        bot.send_message(chat_id, "You have not set your gender, university, partner gender and partner university preferences. Please use the /gender, /uni, /partnergender and /partneruni commands to set them.")
        return

    # Get the user's gender, uni, partner gender and partner uni preferences
    gender = user[1]
    uni = user[2]
    partner_gender = user[3]
    partner_uni = user[4]

    # Search for a partner with matching preferences
    c.execute('SELECT * FROM users WHERE gender=? AND uni=? AND partner_gender=? AND partner_uni=? AND id!=?', (partner_gender, partner_uni, gender, uni, chat_id))
    partner = c.fetchone()

    # If a partner is found
    if partner is not None:
        bot.send_message(chat_id, "Connecting you with a partner...")
        bot.send_message(partner[0], "Connecting you with a partner...")
        bot.send_message(chat_id, "You are now connected with a partner. You can start chatting now.")
        bot.send_message(partner[0], "You are now connected with a partner. You can start chatting now.")
    else:
        bot.send_message(chat_id, "Sorry, no partner found with matching preferences.")

# Handle the /stop command
@bot.message_handler(commands=['stop'])
def stop(message):
    # Get the user's chat ID
    chat_id = message.chat.id

    # Check if the user is currently in a chat
    c.execute('SELECT * FROM chats WHERE user1=? OR user2=?', (chat_id, chat_id))
    chat = c.fetchone()
    if chat is None:
        bot.send_message(chat_id, "You are not currently in a chat.")
        return

    # Get the other user's chat ID
    if chat[1] == chat_id:
        other_user = chat[2]
    else:
        other_user = chat[1]

    # Delete the chat from the chats table
    c.execute('DELETE FROM chats WHERE user1=? AND user2=?', (chat[1], chat[2]))
    conn.commit()

    # Send a message to the user to let them know the chat has been stopped
    bot.send_message(chat_id, "The chat has been stopped.")
    bot.send_message(other_user, "The chat has been stopped.")

#contact
@bot.message_handler(commands=['contact'])
def contact(message):
    bot.send_message(message.chat.id, "Please contact our administrator at admin@example.com for any assistance or questions.")

bot.polling()