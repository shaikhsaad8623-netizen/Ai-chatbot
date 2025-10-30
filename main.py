import telebot
import requests
from flask import Flask
import threading

# 🔑 Your keys
TELEGRAM_TOKEN = "8404990748:AAG0P2QBKz3_Jpqn_0wb94E1MmwBZxmmXZ8"
OPENROUTER_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# 🌐 Flask route (for keeping app alive)
@app.route('/')
def home():
    return "🤖 Saad AI Chatbot is running on Railway!"

# 🤖 AI Chat Function
def ask_ai(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200:
        return res.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error: {res.text}"

# 📩 Handle Telegram messages
@bot.message_handler(func=lambda m: True)
def reply_user(msg):
    bot.send_chat_action(msg.chat.id, "typing")
    reply = ask_ai(msg.text)
    bot.reply_to(msg, reply)

# 🚀 Run Telegram bot in background
def start_bot():
    print("🤖 Bot running...")
    bot.polling(non_stop=True)

# 🏃 Run both Flask and Bot together
if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    app.run(host="0.0.0.0", port=8000)
