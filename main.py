import os
from telegram import Update, Bot, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 6010980234  
YOUTUBE_LINK = "https://youtube.com/@banglaentertainment077?si=QsjcxZlR2S-eQRvh"

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 স্বাগতম!\n\nএই চ্যানেলে যোগ দিতে হলে প্রথমে আমাদের ইউটিউব চ্যানেল সাবস্ক্রাইব করুন:\n{YOUTUBE_LINK}\n\nসাবস্ক্রাইব করার পর স্ক্রিনশট দিন 📸"
    )
    user_data[update.effective_user.id] = {"step": "awaiting_screenshot"}

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_data and user_data[user_id]["step"] == "awaiting_screenshot":
        photo_file = update.message.photo[-1].file_id
        caption = f"✅ Join request from @{update.effective_user.username or 'NoUsername'} (ID: {user_id})\nApprove?"
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo_file, caption=caption)
        await update.message.reply_text("✅ ধন্যবাদ! আপনার রিকোয়েস্ট অ্যাডমিনের কাছে পাঠানো হয়েছে।")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ দয়া করে প্রথমে /start কমান্ড ব্যবহার করুন।")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))
    app.run_polling()
