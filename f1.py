import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
import threading
import time
import requests

# =====================================================================
# 🌐 SERVER REJIMIDA BOTNI 24/7 UYQOQ TUTISH UCHUN TIZIM
# =====================================================================
def keep_alive():
    while True:
        try:
            requests.get("https://google.com")
        except Exception as e:
            print(f"Keep-alive xatosi: {e}")
        time.sleep(600)

threading.Thread(target=keep_alive, daemon=True).start()

# =====================================================================
# ⚙️ BOT SOZLAMALARI VA TOKENLAR
# =====================================================================
API_TOKEN = '8877192617:AAGKNS5OJoPtdO3f8uZawoHLt1s07G-1Gd0'
ADMIN_ID = 8608832630  # Sening shaxsiy ID'ing

bot = telebot.TeleBot(API_TOKEN, parse_mode='HTML')

user_states = {}
# Adminning har bir chatda oxirgi marta xabar yozgan vaqti: {chat_id: timestamp}
admin_last_message_time = {}

# 🌟 Asosiy Menyu
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    portfolio_url = "https://kazajonykk-del.github.io/portfolio/"
    
    web_button = InlineKeyboardButton(text="🚀 INTERAKTIV PORTFOLIO (WEB APP) 🚀", web_app=WebAppInfo(url=portfolio_url))
    markup.add(web_button)
    
    btn_projects = InlineKeyboardButton(text="💻 Saralangan Loyihalarim", callback_data="my_projects")
    btn_order = InlineKeyboardButton(text="🔥 Loyiha Buyurtma Berish", callback_data="make_order")
    btn_socials = InlineKeyboardButton(text="📱 Ijtimoiy Tarmoqlarim", callback_data="my_socials")
    btn_location = InlineKeyboardButton(text="📍 Geografiya / Manzil", callback_data="my_location")
    
    markup.row(btn_projects, btn_order)
    markup.row(btn_socials, btn_location)
    return markup

# =====================================================================
# ⚡️ AQLLI KOTIB REJIMI: 5 DAQIQA YOZMASANGIZ BOT QAYTA ISHLAB KETADI
# =====================================================================
@bot.business_message_handler(func=lambda message: True)
def handle_business_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    business_connection_id = message.business_connection_id
    user_name = message.from_user.first_name
    current_time = time.time()

    # 1. AGAR O'ZING YOZAYOTGAN BO'LSANGIZ: Oxirgi yozgan vaqtingizni saqlaymiz va bot jim turadi
    if user_id == ADMIN_ID:
        admin_last_message_time[chat_id] = current_time
        return

    # Bot javob berishi kerakmi yoki yo'qligini tekshiramiz
    should_respond = True
    
    if chat_id in admin_last_message_time:
        last_time = admin_last_message_time[chat_id]
        # Agar admin oxirgi marta xabar yozganiga 300 soniya (5 daqiqa) to'lmagan bo'lsa - bot jim turadi
        if current_time - last_time < 300:
            should_respond = False

    # 2. AGAR SEN 5 DAQIQADAN BERI YOZMAGAN BO'LSANG: Bot srazu javob beradi
    if should_respond:
        auto_text = (
            f"<b>👋 Salom, {user_name}!</b>\n\n"
            f"Hozirda @RnFlexx band bo'lgani uchun uning raqamli yordamchisi sifatida men javob beryapman. 🤖✨\n\n"
            f"Agar uning ishlari va portfoliosi bilan qiziqsangiz yoki buyurtma bermoqchi bo'lsangiz, "
            f"mening shaxsiy botimga o'tib to'liq ma'lumot olishingiz mumkin: @{bot.get_me().username}\n\n"
            f"<i>Xabaringiz unga yetkazildi, telefonini qo'liga olishi bilan shaxsan o'zi aloqaga chiqadi! 🙏</i>"
        )

        try:
            bot.send_message(
                chat_id=chat_id, 
                text=auto_text, 
                business_connection_id=business_connection_id
            )
        except Exception as e:
            print(f"Biznes xabar yuborishda xato: {e}")

# =====================================================================
# 🤖 BOTNING O'ZIGA KIRGAN FOYDALANUVCHILAR UCHUN INTERFEYS
# =====================================================================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id in user_states:
        user_states.pop(message.chat.id)
        
    welcome_text = (
        f"<b>🚀 Xush kelibsiz, {message.from_user.first_name}!</b>\n\n"
        f"Siz Full-stack dasturchi — <b>Azizbek Fayzullayevning (@RnFlexx)</b> rasmiy portfolio botiga kardingiz.\n\n"
        f"⚡️ Quyidagi tugmalar orqali loyihalarimni ko'rishingiz yoki buyurtma berishingiz mumkin!"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    code = call.data
    if code == 'back_to_menu':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="✨ <b>Asosiy bosh menyu. O'zingizga kerakli bo'limni tanlang:</b>", reply_markup=main_menu())
    elif code == 'my_projects':
        projects_text = (
            "<b>💻 MASHHUR VA REAL LOYIHALARIM:</b>\n\n"
            "🍏 <b>Olcha Cafe</b> — Kafe va restoranlar uchun maxsus, QR-menyu va buyurtmalarni boshqarish tizimi.\n\n"
            "⚡️ <b>Sambu (Welixma)</b> — Yuqori tezlikda ishlovchi zamonaviy platforma.\n\n"
            "<i>💡 Jonli (Live) rejimda sinab ko'rish:</i>"
        )
        proj_kb = InlineKeyboardMarkup(row_width=1)
        proj_kb.add(
            InlineKeyboardButton(text="🟢 Olcha Cafe Saytini Ko'rish", url="https://kazajonykk-del.github.io/olcha/"),
            InlineKeyboardButton(text="🟣 Sambu (Welixma) Saytini Ko'rish", url="https://welixma.vercel.app/"),
            InlineKeyboardButton(text="⬅️ Bosh Menyoga Qaytish", callback_data="back_to_menu")
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=projects_text, reply_markup=proj_kb)
    elif code == 'my_socials':
        social_kb = InlineKeyboardMarkup(row_width=1)
        social_kb.add(
            InlineKeyboardButton(text="📸 Rasmiy Instagram Profilim", url="https://www.instagram.com/rn.flexx/"),
            InlineKeyboardButton(text="💻 Professional GitHub Profilim", url="https://github.com/kazajonykk-del/"),
            InlineKeyboardButton(text="⬅️ Bosh Menyoga Qaytish", callback_data="back_to_menu")
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>📱 Ijtimoiy tarmoqlarim:</b>", reply_markup=social_kb)
    elif code == 'my_location':
        loc_text = "<b>📍 GEO-LOKATSIYA VA MANZIL:</b>\n\nNamangan, Chust tumani."
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text="⬅️ Bosh Menyoga Qaytish", callback_data="back_to_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=loc_text, reply_markup=kb)
    elif code == 'make_order':
        user_states[call.message.chat.id] = {'step': 'name'}
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>🔥 Ismingizni yozing:</b>")

@bot.message_handler(func=lambda message: message.chat.id in user_states)
def order_flow(message):
    chat_id = message.chat.id
    state = user_states[chat_id]
    if state['step'] == 'name':
        state['name'] = message.text
        state['step'] = 'phone'
        bot.send_message(chat_id, "<b>⚡️ Telefon raqamingizni kiriting:</b>")
    elif state['step'] == 'phone':
        state['phone'] = message.text
        state['step'] = 'project_type'
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.row(KeyboardButton("🤖 Telegram Bot"), KeyboardButton("🌐 Web-sayt"))
        bot.send_message(chat_id, "📁 <b>Loyiha turini tanlang:</b>", reply_markup=kb)
    elif state['step'] == 'project_type':
        state['project_type'] = message.text
        state['step'] = 'details'
        hide_kb = telebot.types.ReplyKeyboardRemove()
        bot.send_message(chat_id, "💬 <b>Batafsil ma'lumot bering:</b>", reply_markup=hide_kb)
    elif state['step'] == 'details':
        state['details'] = message.text
        bot.send_message(chat_id, "<b>🎉 Ma'lumotlar qabul qilindi!</b>", reply_markup=main_menu())
        report = f"<b>🚨 YANGI BUYURTMA!</b>\n\n👤 {state['name']}\n📞 {state['phone']}\n🛠 {state['project_type']}\n📝 {state['details']}"
        try: bot.send_message(ADMIN_ID, report)
        except: pass
        user_states.pop(chat_id)

if __name__ == '__main__':
    bot.infinity_polling()