import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os

# تحميل التوكن من ملف .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_ID = 5435422706  # معرف المستخدم الخاص بك لاستقبال الاشتراكات
CHANNEL_USERNAME = "@KanzInternetFree"  # قناة المستخدم

bot = telebot.TeleBot(TOKEN)

# القوائم الرئيسية للعروض
main_menu = {
    "📌 عروض فودافون بيزنس": "vodafone_business",
    "📌 عروض الإنترنت المنزلي أورانج": "orange_internet",
    "📌 عرض باقة 260 فليكس": "flex_260"
}

vodafone_business_offers = {
    "1️⃣ باقة 2500 فليكس - 65 جنيه": "business_2500",
    "2️⃣ باقة 3500 فليكس - 110 جنيه": "business_3500",
    "3️⃣ باقة 6000 فليكس - 160 جنيه": "business_6000"
}

orange_internet_offers = {
    "🌐 200 جيجا - 185 جنيه": "orange_200",
    "🌐 500 جيجا - 230 جنيه": "orange_500",
    "🌐 600 جيجا - 268 جنيه": "orange_600",
    "🌐 1000 جيجا - 338 جنيه": "orange_1000"
}

flex_260_offers = {
    "🔹 13000 فليكس - 200 جنيه": "flex_13000",
    "🔹 5200 فليكس - 80 جنيه": "flex_5200",
    "🔹 2600 فليكس - 60 جنيه": "flex_2600",
    "🔹 الباكدج الكاملة - 350 جنيه": "flex_package"
}

# التحقق من الاشتراك في القناة
def is_subscribed(user_id):
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False

# عرض القائمة الرئيسية
@bot.message_handler(commands=['start'])
def send_main_menu(message):
    user_id = message.from_user.id
    if not is_subscribed(user_id):
        bot.send_message(user_id, f"❌ يجب عليك الانضمام إلى قناتنا أولاً: {CHANNEL_USERNAME}\nثم أعد تشغيل البوت بكتابة /start")
        return

    markup = InlineKeyboardMarkup()
    for text, callback_data in main_menu.items():
        markup.add(InlineKeyboardButton(text, callback_data=callback_data))

    bot.send_message(user_id, "📢 *اختر العرض الذي تريده:*", reply_markup=markup, parse_mode="Markdown")

# معالجة الاختيارات
@bot.callback_query_handler(func=lambda call: True)
def handle_menu_selection(call):
    user_id = call.from_user.id

    if call.data == "vodafone_business":
        send_offer_list(user_id, vodafone_business_offers, "📌 عروض فودافون بيزنس:")
    elif call.data == "orange_internet":
        send_offer_list(user_id, orange_internet_offers, "📌 عروض الإنترنت المنزلي أورانج:")
    elif call.data == "flex_260":
        send_offer_list(user_id, flex_260_offers, "📌 عرض باقة 260 فليكس:")
    else:
        handle_offer_selection(call)

# إرسال قائمة العروض الفرعية
def send_offer_list(user_id, offers, title):
    markup = InlineKeyboardMarkup()
    for text, callback_data in offers.items():
        markup.add(InlineKeyboardButton(text, callback_data=callback_data))

    bot.send_message(user_id, title, reply_markup=markup, parse_mode="Markdown")

# معالجة اختيار الباقات
def handle_offer_selection(call):
    user_id = call.from_user.id
    offer_details = {
        "business_2500": "✅ باقة 2500 فليكس - 65 جنيه\n- 2500 فليكس\n- 500 ميجا فيسبوك\n- 1500 دقيقة وواتساب مجاني",
        "business_3500": "✅ باقة 3500 فليكس - 110 جنيه\n- 3500 فليكس\n- 1000 ميجا فيسبوك\n- 1500 دقيقة وواتساب مجاني",
        "business_6000": "✅ باقة 6000 فليكس - 160 جنيه\n- 6000 فليكس\n- 1500 ميجا فيسبوك\n- 1500 دقيقة وواتساب مجاني",
        "orange_200": "🌐 باقة 200 جيجا - 185 جنيه بدل 330.6 جنيه",
        "orange_500": "🌐 باقة 500 جيجا - 230 جنيه بدل 410.4 جنيه",
        "orange_600": "🌐 باقة 600 جيجا - 268 جنيه بدل 649.8 جنيه",
        "orange_1000": "🌐 باقة 1000 جيجا - 338 جنيه بدل 1550.4 جنيه",
        "flex_13000": "🔹 13000 فليكس - 200 جنيه",
        "flex_5200": "🔹 5200 فليكس - 80 جنيه",
        "flex_2600": "🔹 2600 فليكس - 60 جنيه",
        "flex_package": "🔹 الباكدج الكاملة - 350 جنيه"
    }

    if call.data in offer_details:
        offer_text = f"📢 *تفاصيل العرض:*\n\n{offer_details[call.data]}\n\n📌 *لإتمام الاشتراك، أرسل:*"
        
        if call.data.startswith("flex_"):
            offer_text += "\nأنا فودافون\nرقمي: 0123456789\n📢 رقم وباسورد الأفراد إن وجدوا"
        else:
            offer_text += "\nأنا فودافون\nرقمي: 0123456789"

        bot.send_message(user_id, offer_text, parse_mode="Markdown")

# استقبال بيانات الاشتراك
@bot.message_handler(func=lambda message: "أنا فودافون" in message.text)
def process_subscription(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "✅ *تم استلام طلبك، سيتم التفعيل قريبًا.*\nشكراً لاختيارك عروضنا!", parse_mode="Markdown")

    # إرسال البيانات إلى الأدمين
    admin_message = f"📢 *طلب اشتراك جديد!*\n\n👤 المستخدم: @{message.from_user.username if message.from_user.username else 'بدون اسم مستخدم'}\n🆔 معرفه: {user_id}\n\n📜 *البيانات المستلمة:* \n{message.text}"
    bot.send_message(ADMIN_ID, admin_message, parse_mode="Markdown")

# تشغيل البوت
print("✅ البوت يعمل...")
bot.polling(none_stop=True)
