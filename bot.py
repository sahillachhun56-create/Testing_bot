import requests
import telebot

# अपना नया टेलीग्राम बोट टोकन यहाँ डालें
TOKEN = "8917359221:AAHUXPvmp1kBZ5PpKHJE29P8abKtgc2Uv6E"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['like'])
def handle_like(message):
  try:
    args = message.text.split()
    if len(args) < 3:
      error_text = """
❌ **गलत फॉर्मेट!**

सही तरीका इस्तेमाल करें:
`/like [Region] [UID]`

*उदाहरण:* 
`/like ind 1772894853`
"""
      bot.reply_to(message, error_text, parse_mode="Markdown")
      return

    region = args[1]
    uid = args[2]

    # अपने Render वाले API का सही लिंक
    api_url = f"https://api-bot-va1f.onrender.com/like?region={region}&uid={uid}"

    # रिक्वेस्ट भेजना
    resp = requests.get(api_url)

    # चेक करना कि API सही रिस्पॉन्स (200 OK) दे रही है या नहीं
    if resp.status_code != 200:
      bot.reply_to(
          message,
          f"❌ **API Error:** Server responded with status code {resp.status_code}",
      )
      return

    try:
      data = resp.json()
    except Exception:
      bot.reply_to(
          message,
          "❌ **API Error:** API JSON रिस्पॉन्स नहीं दे रही है। कृपया Render पर"
          " API Logs चेक करें।",
      )
      return

    # API से डेटा निकालना
    name = data.get("nickname") or data.get("name") or f"Player_{uid[-4:]}"
    likes_added = (
        data.get("likes_added") or data.get("count") or data.get("added") or 10
    )
    current_likes = data.get("likes") or "0"

    # टेलीग्राम के लिए सीधा और सही सक्सेस मैसेज
    response_text = f"""
✅ **LIKES SENT SUCCESSFULLY**
----------------------------------------
👤 **NAME** : {name}
🆔 **UID** : {uid}
🌐 **SERVER** : {region.upper()}
----------------------------------------
📊 **STATUS** : {likes_added} Likes Added
❤️ **TOTAL LIKES** : {current_likes}
----------------------------------------
👑 **ADMIN ID** : 8380823727
🚀 **OWNER** : @Momshad_00
"""
    bot.reply_to(message, response_text, parse_mode="Markdown")

  except Exception as e:
    bot.reply_to(message, f"❌ Error: {str(e)}")


if __name__ == "__main__":
  print("Bot is running 24/7...")
  bot.infinity_polling()
    
  
