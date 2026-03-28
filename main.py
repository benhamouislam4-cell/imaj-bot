import cv2
import numpy as np
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- 1. ضَع التوكن الخاص بك هنا ---
TOKEN = "8764560809:AAGIP_1z_xFZv5TMezYEemYSZTnI5P-VznY"

# --- 2. وظيفة معالجة وتجميل الصورة (التي شرحناها في الخطوة 3) ---
def process_image(input_path, output_path):
    img = cv2.imread(input_path)
    # تنعيم البشرة
    beauty = cv2.bilateralFilter(img, 15, 75, 75)
    # زيادة الحدة (Sharpening)
    gaussian_3 = cv2.GaussianBlur(beauty, (0, 0), 2.0)
    unsharp = cv2.addWeighted(beauty, 1.5, gaussian_3, -0.5, 0)
    # تعديل الألوان السينمائي
    hsv = cv2.cvtColor(unsharp, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], 1.3) # زيادة التشبع
    final_img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    cv2.imwrite(output_path, final_img)

# --- 3. وظيفة استقبال الصور من المستخدم ---
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إخبار المستخدم أن البوت يعمل
    await update.message.reply_text("جاري تجميل صورتك بأسلوب سينمائي.. انتظر قليلاً 🚀")
    
    # تحميل الصورة التي أرسلها المستخدم
    photo_file = await update.message.photo[-1].get_file()
    input_file = "user_input.jpg"
    output_file = "top_ramy_result.jpg"
    await photo_file.download_to_drive(input_file)

    # معالجة الصورة بالكود الخاص بنا
    process_image(input_file, output_file)

    # إرسال الصورة الناتجة للمستخدم
    with open(output_file, 'rb') as f:
        await update.message.reply_photo(photo=f, caption="تم التجميل بنجاح! جودة سينمائية لـ TOP RAMY ✨")

# --- 4. تشغيل البوت ---
if __name__ == '__main__':
    print("البوت يعمل الآن...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
