import os
from threading import Thread
from flask import Flask
import requests
import telebot

# Port Binding for Render
app = Flask("")


@app.route("/")
def home():
  return "Telegram Bot is Alive!"


def run():
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)


def keep_alive():
  t = Thread(target=run)
  t.start()


# टेलीग्राम बोट टोकन
TOKEN = "8917359221:AAHJbJR-ifKaUBOq-nNmyR_wR9h_thJq860"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["like"])
def handle_like(message):
  try:
    args = message.text.split()
    if len(args) < 3:
      error_text = (
          "❌ गलत फॉर्मेट!\n\nसही तरीका इस्तेमाल करें:\n/like [Region]"
          " [UID]\n\nउदाहरण:\n/like ind 1772894853"
      )
      bot.reply_to(message, error_text)
      return

    region = args[1]
    uid = args[2]

    api_url = f"https://api-bot-va1f.onrender.com/like?region={region}&uid={uid}&key=Anurag"
    resp = requests.get(api_url)

    if resp.status_code != 200:
      bot.reply_to(
          message,
          f"❌ API Error: सर्वर व्यस्त है (Status {resp.status_code})।",
      )
      return

    try:
      data = resp.json()
    except Exception:
      bot.reply_to(message, "❌ API Error: सर्वर से सही JSON नहीं मिला।")
      return

    name = data.get("nickname") or data.get("name") or "N/A"
    likes_added = (
        data.get("likes_added") or data.get("count") or data.get("added") or 10
    )
    current_likes = data.get("likes") or "N/A"

    response_text = f"""
✅ LIKES SENT SUCCESSFULLY
----------------------------------------
👤 NAME : {name}
🆔 UID : {uid}
🌐 SERVER : {region.upper()}
----------------------------------------
📊 STATUS : {likes_added} Likes Added
❤️ TOTAL LIKES : {current_likes}
----------------------------------------
👑 ADMIN ID : 8380823727
🚀 OWNER : @Momshad_00
"""
    bot.reply_to(message, response_text)

  except Exception as e:
    bot.reply_to(message, f"❌ Error: {str(e)}")


if __name__ == "__main__":
  keep_alive()  # Render Port Fix
  print("Bot is running 24/7...")
  bot.infinity_polling()
  
  
    
  
