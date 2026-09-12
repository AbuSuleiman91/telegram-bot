import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ضع التوكن الخاص ببوتك من BotFather هنا
TOKEN = "8736545912:AAHBdIgtMtC0_1DfE1rOuGbujEgvpCzot5w"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أرسل لي أي يوزر (username) لجمع البيانات المتاحة عنه.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # التحقق مما إذا كان المدخل يوزر
    if text.startswith("@") or not text.startswith("http"):
        username = text.replace("@", "")
        
        # استجابة توضيحية تجريبية
        response = (
            f"📊 **معلومات الحساب :** @{username}\n\n"
            f"👤 **اسم المستخدم:** {username}\n"
            f"ℹ️ **الحالة:** جاري المعالجة...\n\n"
            f"⚠️ ملاحظة: جلب البيانات الخاصة مثل رقم الهاتف أو الإيميل غير المتاح للعامة يتطلب صلاحيات API خاصة من المنصة."
        )
        await update.message.reply_text(response, parse_mode="Markdown")
    else:
        await update.message.reply_text("الرجاء إرسال اسم مستخدم صحيح.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("البوت يعمل الآن...")
    app.run_polling()
