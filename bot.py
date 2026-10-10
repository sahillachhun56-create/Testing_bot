import requests
import telebot

# अपना नया टेलीग्राम बोट टोकन यहाँ डालें
TOKEN = "8917359221:AAFjeB-y849GIFjraA5wWpu8caiuOqjSTYk"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['like'])
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

    # अपने Render वाले API का लिंक
    api_url = f"https://api-bot-va1f.onrender.com/like?region={region}&uid={uid}"

    # रिक्वेस्ट भेजना
    resp = requests.get(api_url)

    if resp.status_code != 200:
      bot.reply_to(
          message,
          f"❌ API Error: सर्वर व्यस्त है या रिस्पॉन्स कोड {resp.status_code}"
          " मिला। कृपया दोबारा ट्राई करें।",
      )
      return

    try:
      data = resp.json()
    except Exception:
      bot.reply_to(
          message,
          "❌ API Error: सर्वर से सही डेटा नहीं मिला। कृपया Render लॉग्स चेक"
          " करें।",
      )
      return

    # API से डेटा निकालना
    name = data.get("nickname") or data.get("name") or f"Player_{uid[-4:]}"
    likes_added = (
        data.get("likes_added") or data.get("count") or data.get("added") or 10
    )
    current_likes = data.get("likes") or "0"

    # सादा टेक्स्ट मैसेज (बिنا किसी Markdown एरर के)
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
  print("Bot is running 24/7...")
  bot.infinity_polling()
  
    
  
