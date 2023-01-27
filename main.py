import sqlite3
from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text("Welcome to Anonymous Chat Bot! Please use the /gender command to choose your gender and /uni command to choose your university.")

def gender(update, context):
    user_id = update.message.from_user.id
    user_gender = context.args[0]
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if result:
        c.execute("UPDATE users SET gender = ? WHERE user_id = ?", (user_gender, user_id))
    else:
        c.execute("INSERT INTO users (user_id, gender) VALUES (?, ?)", (user_id, user_gender))
    conn.commit()
    conn.close()
    update.message.reply_text("Your gender has been set to " + user_gender + ". Please use the /uni command to choose your university.")

def uni(update, context):
    user_id = update.message.from_user.id
    user_uni = context.args[0]
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET uni = ? WHERE user_id = ?", (user_uni, user_id))
    conn.commit()
    conn.close()
    update.message.reply_text("Your university has been set to " + user_uni + ". You can now use the /partnergender and /partneruni commands to choose your preferred gender and university for a partner.")

def partnergender(update, context):
    user_id = update.message.from_user.id
    partner_gender = context.args[0]
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET partnergender = ? WHERE user_id = ?", (partner_gender, user_id))
    conn.commit()
    conn.close()
    update.message.reply_text("Your partner gender preference has been set to " + partner_gender + ". You can now use the /partneruni command to choose your preferred university for a partner.")

def partneruni(update, context):
    user_id = update.message.from_user.id
    partner_uni = context.args[0]
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET partneruni = ? WHERE user_id = ?", (partner_uni, user_id))
    conn.commit()
    conn.close()
    update.message.reply_text("Your partner university preference has been set to " + partner_uni + ". You can now use the /start command to begin searching for a partner.")

def report(update, context):
    user_id = update.message.from_user.id
    report_text = context.args[0]
    conn = sqlite3.    connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO reports (user_id, report_text) VALUES (?, ?)", (user_id, report_text))
    conn.commit()
    conn.close()
    update.message.reply_text("Thank you for your report. Our team will look into it.")

def stop(update, context):
    user_id = update.message.from_user.id
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("DELETE FROM chats WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    update.message.reply_text("Your current chat has been stopped.")

def profile(update, context):
    user_id = update.message.from_user.id
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if result:
        update.message.reply_text("Your current profile settings: \nGender: " + result[1] + "\nUniversity: " + result[2] + "\nPartner Gender Preference: " + result[3] + "\nPartner University Preference: " + result[4])
    else:
        update.message.reply_text("You have not set up your profile yet. Please use the /gender and /uni commands to set up your profile.")

def contact(update, context):
    update.message.reply_text("If you need to contact the administrator, please email us at admin@anonymouschatbot.com.")

def connect(update, context):
    user_id = update.message.from_user.id
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if result:
        gender = result[1]
        uni = result[2]
        partnergender = result[3]
        partneruni = result[4]
        c.execute("SELECT user_id FROM users WHERE gender = ? AND uni = ? AND partnergender = ? AND partneruni = ?", (gender, uni, partnergender, partneruni))
        partner = c.fetchone()
        if partner:
            c.execute("INSERT INTO chats (user_id, partner_id) VALUES (?, ?)", (user_id, partner[0]))
            conn.commit()
            update.message.reply_text("You have been connected with a partner. You can start chatting now.")
        else:
            update.message.reply_text("Sorry, we could not find a matching partner for you at this time. Please try again later.")
    else:
        update.message.reply_text("You have not set up your profile yet. Please use the /gender and /uni commands to set up your profile.")
    conn.close()

def main():
    updater = Updater("5436395817:AAFngaB7h9MsHc1fA8et4sFOWVEPJ04WkOI", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("gender", gender))
    dp.add_handler(CommandHandler("uni", uni))
    dp.add_handler(CommandHandler("partnergender", partnergender))
    dp.add_handler(CommandHandler("partneruni", partneruni))
    dp.add_handler(CommandHandler("report", report))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("profile", profile))
    dp.add_handler(CommandHandler("connect", connect))
    dp.add_handler(CommandHandler("contact", contact))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
