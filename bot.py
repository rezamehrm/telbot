import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# ==================== تنظیمات شما ====================
BOT_TOKEN = "7363392477:AAEHHx6C3MAhCQVryRKKD7G2_lgEVeArkTw"
CHANNEL_USERNAME = "@estelajii"
GROUP_USERNAME = "@estlji"
SERVICE_NAME = "پشتیبانی استعلاجی"
ADMIN_ID = 7158635583
# ====================================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def check_membership(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """بررسی عضویت کاربر در کانال و گروه"""
    try:
        channel_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        group_member = await context.bot.get_chat_member(GROUP_USERNAME, user_id)
        
        valid_statuses = ['member', 'administrator', 'creator']
        channel_ok = channel_member.status in valid_statuses
        group_ok = group_member.status in valid_statuses
        
        return channel_ok and group_ok
    except Exception as e:
        logging.error(f"خطا در بررسی عضویت: {e}")
        return False

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """فوروارد پیام به ادمین"""
    try:
        user = update.effective_user
        user_info = f"👤 کاربر: {user.first_name} ({user.id})"
        if user.username:
            user_info += f" - @{user.username}"
        
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 پیام جدید از {SERVICE_NAME}\n{user_info}"
        )
        await context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
    except Exception as e:
        logging.error(f"خطا در فوروارد به ادمین: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /start"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    if await check_membership(user_id, context):
        await update.message.reply_text(
            f"✅ سلام {user_name} عزیز!\n"
            f"از اینکه در کانال و گروه {SERVICE_NAME} عضو هستید متشکریم.\n\n"
            f"📝 اکنون می‌توانید سوال یا پیام پشتیبانی خود را ارسال کنید."
        )
    else:
        keyboard = [
            [InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton("👥 عضویت در گروه", url=f"https://t.me/{GROUP_USERNAME[1:]}")],
            [InlineKeyboardButton("🔍 بررسی عضویت", callback_data="check_membership")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"⚠️ سلام {user_name} عزیز!\n"
            f"برای استفاده از ربات {SERVICE_NAME} و ارسال پیام، باید ابتدا در کانال و گروه ما عضو شوید.\n\n"
            "✅ پس از عضویت، روی دکمه «بررسی عضویت» کلیک کنید.\n"
            "🔒 پس از تایید عضویت، می‌توانید پیام خود را ارسال کنید.",
            reply_markup=reply_markup
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش پیام‌های کاربر"""
    user_id = update.effective_user.id
    
    # نادیده گرفتن دستورات
    if update.message.text and update.message.text.startswith('/'):
        return

    if await check_membership(user_id, context):
        # کاربر عضو است - فوروارد پیام به ادمین
        await forward_to_admin(update, context)
        await update.message.reply_text(
            "✅ پیام شما دریافت شد و به تیم پشتیبانی ارسال گردید.\n"
            "🕐 به زودی با شما تماس گرفته خواهد شد.\n\n"
            "🙏 از صبر و شکیبایی شما متشکریم."
        )
    else:
        # کاربر عضو نیست - حذف پیام و اخطار
        await update.message.delete()
        
        keyboard = [[InlineKeyboardButton("🔍 بررسی مجدد عضویت", callback_data="check_membership")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        warning_msg = await update.message.reply_text(
            "❌ شما هنوز در کانال و/یا گروه ما عضو نیستید!\n\n"
            "⚠️ لطفاً ابتدا با استفاده از دکمه‌های بالا عضو شوید و سپس مجدداً تلاش کنید.",
            reply_markup=reply_markup
        )
        
        # حذف پیام اخطار بعد از 10 ثانیه
        await asyncio.sleep(10)
        try:
            await warning_msg.delete()
        except:
            pass

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت کلیک روی دکمه"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_name = query.from_user.first_name
    
    if await check_membership(user_id, context):
        await query.edit_message_text(
            f"✅ سلام {user_name} عزیز!\n"
            f"عضویت شما تایید شد! 🎉\n\n"
            f"📝 اکنون می‌توانید پیام پشتیبانی خود را ارسال کنید."
        )
    else:
        keyboard = [
            [InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton("👥 عضویت در گروه", url=f"https://t.me/{GROUP_USERNAME[1:]}")],
            [InlineKeyboardButton("🔍 بررسی مجدد", callback_data="check_membership")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"❌ متأسفیم {user_name} عزیز!\n"
            f"هنوز در کانال و/یا گروه ما عضو نیستید.\n\n"
            f"⚠️ لطفاً از دکمه‌های بالا برای عضویت استفاده کنید و سپس بررسی نمایید.",
            reply_markup=reply_markup
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت خطاها"""
    logging.error(f"خطا رخ داد: {context.error}")

def main():
    """تابع اصلی"""
    print(f"🚀 در حال راه‌اندازی ربات {SERVICE_NAME}...")
    print(f"📊 کانال: {CHANNEL_USERNAME}")
    print(f"📊 گروه: {GROUP_USERNAME}")
    print(f"👤 ادمین: {ADMIN_ID}")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler, pattern="^check_membership$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    # اجرای ربات
    print("🤖 ربات فعال شد! برای توقف Ctrl+C را بزنید.")
    application.run_polling()

if __name__ == '__main__':
    main()
