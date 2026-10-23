import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ۱. توکن تلگرام و کلید جیمنای خود را اینجا قرار دهید
TELEGRAM_BOT_TOKEN = "8671982483:AAHXExt-3Hw77mj6qGN8bDBK06u20hFoslw"
GEMINI_API_KEY = "AQ.Ab8RN6KAq9o3OYUxKex5J_43nzTYHzdZIURBeGZ85DkOP_YSkA"

# ۲. تنظیم کلید API
genai.configure(api_key=GEMINI_API_KEY)

# ۳. دستورالعمل تخصصی برای هوش مصنوعی (نقش استادیار قرآن)
SYSTEM_PROMPT = """
تو یک استادیار و متخصص حرفه‌ای حفظ قرآن هستی. 
وظیفه تو این است که به استادی که تا جزء ۸ قرآن را حفظ کرده اما آیات متشابه را قاطی می‌کند کمک کنی.
وقتی کاربر آیه‌ای را می‌فرستد:
۱. اگر در مورد متشابهات پرسید، دقیقاً مشخص کن این آیه با کدام آیات دیگر شباهت دارد و تفاوت دقیق کلمات را مشخص کن.
۲. ارتباط معنایی و خط داستانی آیه را خیلی کوتاه و روان توضیح بده.
۳. لحنت بسیار محترمانه، صمیمی، متواضعانه و مشوقانه باشد.
"""

# ۴. ساخت مدل هوش مصنوعی با دستورالعمل بالا
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=SYSTEM_PROMPT
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام استاد عزیز! به دستیار هوشمند حفظ قرآن خوش آمدید.\n\n"
        "هر آیه‌ای که در آن شک دارید یا با آیات دیگر قاطی می‌کنید را بفرستید تا دقیقاً متشابهات، تفاوت‌های کلمه‌ای و خط داستانی آن را برایتان تحلیل کنم."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        # چاپ خطای دقیق در ترمینال و ارسال آن به تلگرام برای بررسی
        print(f"خطای دقیق: {e}")
        await update.message.reply_text(f"خطای فنی جیمنای: {str(e)}")
        
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("ربات با موفقیت فعال شد و آماده پاسخگویی است...")
    app.run_polling()