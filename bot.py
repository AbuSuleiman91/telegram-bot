cat << 'EOF' > bot.py
import logging
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

GEMINI_API_KEY = "AQ.Ab8RN6KkUmO9rL9OYV51ATaPgC7TDj3tr8tG8DEnv8LoisoGRA"
TELEGRAM_BOT_TOKEN = "8457731395:AAGUZ61w0ZylTKDRxAPbVIOaOzZ6a9rpFJc"

client = genai.Client(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أنا مساعدك البرمجي الذكي.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    system_instruction = "أنت مساعد برمجي خبير. قدم حلولاً برمجية دقيقة، شرحاً واضحاً، وكوداً نظيفاً."
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{system_instruction}\n\nسؤال المستخدم: {user_prompt}"
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("البوت يعمل الآن...")
    app.run_polling()
EOF