import json
import urllib.request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

GEMINI_API_KEY = "AQ.Ab8RN6KkUmO9rL9OYV51ATaPgC7TDj3tr8tG8DEnv8LoisoGRA"
TELEGRAM_BOT_TOKEN = "8457731395:AAGUZ61w0ZylTKDRxAPbVIOaOzZ6a9rpFJc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أنا مساعدك البرمجي الذكي.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": f"أنت مساعد برمجي خبير. قدم حلولاً دقيقة وكوداً نظيفاً.\n\nسؤال المستخدم: {user_prompt}"}]
        }]
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            text = result['candidates'][0]['content']['parts'][0]['text']
            await update.message.reply_text(text)
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("البوت يعمل الآن...")
    app.run_polling()