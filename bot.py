import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# ==================== تنظیمات شما ====================
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8588091872:AAG7XZEwWjMB7614B2nigKMGZOqInnMwJWI')
CHANNEL_USERNAME = "@estelajii"
GROUP_USERNAME = "@estlji"
SERVICE_NAME = "پشتیبانی استعلاجی"
ADMIN_ID = 7158635583
SUPPORT_USERNAME = "ervid"
# ====================================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def check_membership(user_id: int, context: CallbackContext) -> bool:
    """بررسی عضویت کاربر در کانال و گروه"""
    try:
        channel_member = context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        group_member = context.bot.get_chat_member(GROUP_USERNAME, user_id)
        
        valid_statuses = ['member', 'administrator', 'creator']
        return (channel_member.status in valid_statuses and 
                group_member.status in valid_statuses)
    except Exception as e:
        logging.error(f"خطا در بررسی عضویت: {e}")
        return False

def start(update: Update, context: CallbackContext):
    """دستور /start"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    if check_membership(user_id, context):
        update.message.reply_text(
            f"✅ سلام {user_name} عزیز!\n"
            f"از اینکه در کانال و گروه {SERVICE_NAME} عضو هستید متشکریم.\n\n"
            f"📝 اکنون می‌توانید سوال یا پیام پشتیبانی خود را ارسال کنید.\n\n"
            f"💎 **جهت مشاوره تخصصی:**\n"
            f"@{SUPPORT_USERNAME}"
        )
    else:
        keyboard = [
            [InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton("👥 عضویت در گروه", url=f"https://t.me/{GROUP_USERNAME[1:]}")],
            [InlineKeyboardButton("🔍 بررسی عضویت", callback_data="check_membership")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(
            f"⚠️ سلام {user_name} عزیز!\n"
            f"برای استفاده از ربات {SERVICE_NAME} و ارسال پیام، باید ابتدا در کانال و گروه ما عضو شوید.\n\n"
            "✅ پس از عضویت، روی دکمه «بررسی عضویت» کلیک کنید.",
            reply_markup=reply_markup
        )

def handle_message(update: Update, context: CallbackContext):
    """پردازش پیام‌های کاربر"""
    user_id = update.effective_user.id
    
    if update.message.text and update.message.text.startswith('/'):
        return

    if check_membership(user_id, context):
        update.message.reply_text(
            "✅ پیام شما دریافت شد!\n\n"
            f"💎 **جهت مشاوره تخصصی با پشتیبان:**\n"
            f"@{SUPPORT_USERNAME}"
        )
    else:
        update.message.delete()
        update.message.reply_text("❌ لطفاً اول عضو شوید!")

def button_handler(update: Update, context: CallbackContext):
    """مدیریت کلیک روی دکمه"""
    query = update.callback_query
    query.answer()
    
    user_id = query.from_user.id
    user_name = query.from_user.first_name
    
    if check_membership(user_id, context):
        query.edit_message_text(
            f"✅ سلام {user_name} عزیز!\n"
            f"عضویت شما تایید شد! 🎉\n\n"
            f"📝 اکنون می‌توانید پیام پشتیبانی خود را ارسال کنید.\n\n"
            f"💎 **جهت مشاوره تخصصی:**\n"
            f"@{SUPPORT_USERNAME}"
        )
    else:
        query.edit_message_text("❌ هنوز عضو نشدید!")

def main():
    """تابع اصلی"""
    print(f"🚀 در حال راه‌اندازی ربات {SERVICE_NAME}...")
    print(f"📊 کانال: {CHANNEL_USERNAME}")
    print(f"📊 گروه: {GROUP_USERNAME}")
    print(f"👤 ادمین: {ADMIN_ID}")
    print(f"💎 پشتیبان: @{SUPPORT_USERNAME}")
    
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler, pattern="^check_membership$"))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    print("✅ ربات فعال شد!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
