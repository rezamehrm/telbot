import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# دریافت توکن از Environment Variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# آیدی کانال و گروه خود را اینجا قرار دهید
CHANNEL_USERNAME = "@username_kanal_shoma"
GROUP_USERNAME = "@username_group_shoma"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def check_membership(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        channel_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        group_member = await context.bot.get_chat_member(GROUP_USERNAME, user_id)
        
        if channel_member.status in ['member', 'administrator', 'creator'] and group_member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        logging.error(f"Error: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await check_membership(user_id, context):
        await update.message.reply_text("✅ عضو هستید! پیام خود را ارسال کنید.")
    else:
        keyboard = [
            [InlineKeyboardButton("📢 کانال", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton("👥 گروه", url=f"https://t.me/{GROUP_USERNAME[1:]}")],
            [InlineKeyboardButton("🔍 بررسی عضویت", callback_data="check")]
        ]
        await update.message.reply_text("لطفا اول عضو شوید:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.message.text and update.message.text.startswith('/'):
        return

    if await check_membership(user_id, context):
        await update.message.reply_text("📩 پیام دریافت شد!")
    else:
        await update.message.delete()
        await update.message.reply_text("❌ عضو نیستید!")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if await check_membership(user_id, context):
        await query.edit_message_text("✅ عضویت تایید شد!")
    else:
        await query.edit_message_text("❌ هنوز عضو نشدید!")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler, pattern="^check$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot running...")
    application.run_polling()

if __name__ == '__main__':
    main()
