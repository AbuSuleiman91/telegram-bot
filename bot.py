import os
import json
import urllib.request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# نقرأ التوكنات من متغيرات البيئة في السيرفر، مو من الكود
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👨‍💻 أهلاً يا مبرمج! أنا Coder Bot جاهز\nارسل كودك أو سؤالك.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    await update.message.reply_text("🧠 قاعد أحلل الكود...")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": "qwen-2.5-coder-32b",
        "messages": [
            {"role": "system", "content": "انت خبير برمجة محترف، تجاوب بالعربي وتكتب كود نظيف."},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2
    }

    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            answer = result['choices'][0]['message']['content']
    except Exception as e:
        answer = f"حدث خطأ: {e}"

    # تقسيم الرسالة الطويلة
    for i in range(0, len(answer), 4000):
        await update.message.reply_text(answer[i:i+4000])

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()