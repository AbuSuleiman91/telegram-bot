import logging
import re
import instaloader
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 1. التوكن الجديد الخاص بك من BotFather
BOT_TOKEN = "ضع_التوكن_الجديد_هنا"

# 2. بيانات حساب إنستغرام الفرعي لتجاوز التقييد (اختياري لكن يفضل استخدامه)
INSTA_USER = "3.e.lr"
INSTA_PASS = "ضع_كلمة_مرور_الحساب_هنا" 

L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    save_metadata=False,
    compress_json=False,
    request_timeout=10.0
)

# محاولة تسجيل الدخول لتجاوز حظر إنستغرام
if INSTA_USER and INSTA_PASS and INSTA_PASS != "ضع_كلمة_مرور_الحساب_هنا":
    try:
        L.login(INSTA_USER, INSTA_PASS)
        print("تم تسجيل الدخول بنجاح إلى إنستغرام!")
    except Exception as e:
        print("تنبيه تسجيل الدخول:", e)

def extract_username(input_text: str) -> str:
    """استخراج اسم المستخدم سواء كان رابطاً أو نصاً عادياً"""
    text = input_text.strip()
    # إذا كان الرابط كاملاً مثل instagram.com/username
    match = re.search(r'instagram\.com/([^/?#&]+)', text)
    if match:
        return match.group(1).replace('@', '').strip()
    # إذا كان النص يوزر عادي
    return text.replace('@', '').strip()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أرسل لي رابط الحساب (Profile URL) أو اسم المستخدم لجلب البيانات المتاحة عنه.")

async def process_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_text = update.message.text
    username = extract_username(raw_text)

    if not username:
        await update.message.reply_text("❌ لم يتم التعرف على اسم المستخدم أو الرابط.")
        return

    status_msg = await update.message.reply_text(f"🔍 جاري جلب بيانات الحساب: {username}...")

    try:
        profile = instaloader.Profile.from_username(L.context, username)
        info_text = (
            f"📊 **معلومات الحساب:**\n\n"
            f"👤 **الاسم:** {profile.full_name}\n"
            f"🔗 **اسم المستخدم:** {profile.username}\n"
            f"👥 **المتابعون:** {profile.followers:,}\n"
            f"➡️ **الذين يتابعهم:** {profile.followees:,}\n"
            f"📸 **عدد المنشورات:** {profile.mediacount:,}\n"
            f"🔒 **حساب خاص:** {'نعم' if profile.is_private else 'لا'}\n"
            f"✅ **حساب موثق:** {'نعم' if profile.is_verified else 'لا'}\n\n"
            f"📝 **البايو:**\n{profile.biography if profile.biography else 'لا يوجد'}"
        )
        await status_msg.edit_text(info_text, parse_mode='Markdown')

    except instaloader.exceptions.ProfileNotExistsException:
        await status_msg.edit_text("❌ اسم المستخدم غير موجود على إنستغرام.")
    except instaloader.exceptions.ConnectionException:
        await status_msg.edit_text("⚠️ تعذر الاتصال بإنستغرام حالياً (يتطلب تسجيل الدخول بحساب فرعي للوصول لهذه البيانات).")
    except Exception as e:
        await status_msg.edit_text(f"❌ حدث خطأ أثناء المعالجة: {str(e)}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_username))
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
