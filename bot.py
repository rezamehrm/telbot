from telegram import Bot
import logging

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8588091872:AAG7XZEwWjMB7614B2nigKMGZOqInnMwJWI"

try:
    print("🔗 در حال تست اتصال...")
    bot = Bot(token=BOT_TOKEN)
    me = bot.get_me()
    print(f"✅ اتصال موفق! ربات: {me.first_name} (@{me.username})")
    print("🎯 توکن معتبر است!")
except Exception as e:
    print(f"❌ خطا: {e}")
