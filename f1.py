import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
import threading
import time
import requests

# =====================================================================
# 🌐 SERVER REJIMIDA BOTNI 24/7 UYQOQ TUTISH UCHUN FUNKSIYA
# =====================================================================
def keep_alive():
    while True:
        try:
            # Bot serverda o'chib qolmasligi uchun har 10 daqiqada tarmoqqa so'rov yuboradi
            requests.get("https://google.com")
        except Exception as e:
            print(f"Keep-alive xatosi: {e}")
        time.sleep(600)  # 600 soniya = 10 daqiqa

# Fondagi uyg'otuvchi tizimni ishga tushirish
threading.Thread(target=keep_alive, daemon=True).start()

# =====================================================================
# ⚙️ BOT SOZLAMALARI VA TOKENDAR
# =====================================================================
API_TOKEN = '8877192617:AAGKNS5OJoPtdO3f8uZawoHLt1s07G-1Gd0'
ADMIN_ID = 8608832630  # Sening shaxsiy ID'ing, buyurtmalar shu yerga keladi

bot = telebot.TeleBot(API_TOKEN, parse_mode='HTML')

# Foydalanuvchilar holatini saqlash (Buyurtma olish tizimi uchun)
user_states = {}

# 🌟 Jozibali va Rangli Asosiy Menyu
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    portfolio_url = "https://kazajonykk-del.github.io/portfolio/"
    
    web_button = InlineKeyboardButton(text="✨ INTERAKTIV PORTFOLIO (WEB APP) ✨", web_app=WebAppInfo(url=portfolio_url))
    markup.add(web_button)
    
    btn_projects = InlineKeyboardButton(text="💻 Real Loyihalarim", callback_data="my_projects")
    btn_order = InlineKeyboardButton(text="🔥 Buyurtma berish", callback_data="make_order")
    btn_socials = InlineKeyboardButton(text="📱 Ijtimoiy Tarmoqlar", callback_data="my_socials")
    btn_location = InlineKeyboardButton(text="📍 Shahar / Manzil", callback_data="my_location")
    
    markup.row(btn_projects, btn_order)
    markup.row(btn_socials, btn_location)
    return markup

# =====================================================================
# ⚡️ KOTIB REJIMI: SHAXSIY PROFILGA YOZILGAN XABARLARGA JAVOB BERISH
# =====================================================================
@bot.business_message_handler(func=lambda message: True)
def handle_business_message(message):
    """ Profilingizga xabar kelganda ishlaydigan aqlli avto-javob """
    chat_id = message.chat.id
    business_connection_id = message.business_connection_id  # Biznes ulanish ID-si
    user_name = message.from_user.first_name

    auto_text = (
        f"<b>🚀 Salom, {user_name}! Assalomu alaykum.</b>\n\n"
        f"Hozirda Azizbek band bo'lishi mumkin. Men uning sun'iy yordamchisiman. 🤖\n\n"
        f"Agar uning ishlari, portfolio yoki loyihalari bilan qiziqayotgan bo'lsangiz yoki buyurtma bermoqchi bo'lsangiz, "
        f"mening shaxsiy botimga o'tib, to'liq ma'lumot olishingiz mumkin: @{bot.get_me().username}\n\n"
        f"<i>Xabaringiz Azizbekka yetkazildi, bo'shashi bilan shaxsan o'zi javob yozadi! ✨</i>"
    )

    try:
        # Shaxsiy profilingiz nomidan mijozga avto-javob yuborish
        bot.send_message(
            chat_id=chat_id, 
            text=auto_text, 
            business_connection_id=business_connection_id
        )
    except Exception as e:
        print(f"Biznes xabar yuborishda xato: {e}")

# =====================================================================
# 🤖 ODDY BOT FUNKSIYALARI (Botning o'ziga kirganlar uchun)
# =====================================================================

# /start komandasi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id in user_states:
        user_states.pop(message.chat.id)
        
    welcome_text = (
        f"<b>🚀 Assalomu alaykum, {message.from_user.first_name}!</b>\n\n"
        "Men Full-stack dasturchi va Bot Creator — <b>Azizbek Fayzullayevning</b> portfolio yordamchi botiman.\n\n"
        "⚡️ Pastdagi tugmalar orqali mening urf bo'lgan ishlarimni ko'rishingiz yoki o'z loyihangiz uchun buyurtma qoldirishingiz mumkin!"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

# Inline tugmalar bosilganda (Callback)
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    code = call.data
    
    if code == 'back_to_menu':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="✨ <b>Asosiy menyu. Kerakli bo'limni tanlang:</b>", reply_markup=main_menu())
        
    elif code == 'my_projects':
        projects_text = (
            "<b>💻 MENING REAL LOYIHALARIM:</b>\n\n"
            "🟢 <b>Olcha Cafe</b> — Restoran va kafelar uchun mukammal raqamli menyu va dashboard tizimi.\n\n"
            "🟣 <b>Sambu (Welixma)</b> — Kreativ va zamonaviy interfeysga ega maxsus platforma.\n\n"
            "<i>💡 Loyihalarni jonli ko'rish uchun pastdagi tugmalarni bosing!</i>"
        )
        proj_kb = InlineKeyboardMarkup(row_width=1)
        proj_kb.add(
            InlineKeyboardButton(text="🍏 Olcha Cafe saytini ko'rish", url="https://kazajonykk-del.github.io/olcha/"),
            InlineKeyboardButton(text="⚡️ Sambu (Welixma) saytini ko'rish", url="https://welixma.vercel.app/"),
            InlineKeyboardButton(text="⬅️ Orqaga qaytish", callback_data="back_to_menu")
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text=projects_text, reply_markup=proj_kb)
        
    elif code == 'my_socials':
        social_kb = InlineKeyboardMarkup(row_width=2)
        social_kb.row(
            InlineKeyboardButton(text="✈️ Telegram Kanal", url="https://t.me/F1AA777"),
            InlineKeyboardButton(text="💻 GitHub Profil", url="https://github.com/kazajonykk-del")
        )
        social_kb.row(
            InlineKeyboardButton(text="📸 Instagram", url="https://instagram.com/f11aa77"),
            InlineKeyboardButton(text="🔵 Facebook", url="https://www.facebook.com/azizbek.fajzullaev.2025?locale=ru_RU")
        )
        social_kb.add(InlineKeyboardButton(text="⬅️ Orqaga qaytish", callback_data="back_to_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="<b>📱 Mening rasmiy ijtimoiy tarmoqlarim:</b>", reply_markup=social_kb)
        
    elif code == 'my_location':
        loc_text = "📍 <b>Manzil:</b> O'zbekiston, Namangan viloyati, Chust tumani.\n\n🌍 Dunyoning istalgan nuqtasidan turib online hamkorlik qilish imkoniyati bor!"
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text="⬅️ Orqaga qaytish", callback_data="back_to_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text=loc_text, reply_markup=kb)
        
    elif code == 'make_order':
        user_states[call.message.chat.id] = {'step': 'name'}
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="<b>🔥 Zo'r! Kelajakdagi loyihangizni portlatamiz!</b>\n\nIsmingiz nima?")

# Buyurtma berish so'rovnomasi (Step-by-Step)
@bot.message_handler(func=lambda message: message.chat.id in user_states)
def order_flow(message):
    chat_id = message.chat.id
    state = user_states[chat_id]
    
    if state['step'] == 'name':
        state['name'] = message.text
        state['step'] = 'phone'
        bot.send_message(chat_id, "⚡️ Ajoyib! Endi <b>Telefon raqamingizni</b> yozing:")
        
    elif state['step'] == 'phone':
        state['phone'] = message.text
        state['step'] = 'project_type'
        
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.row(KeyboardButton("🤖 Telegram Bot"), KeyboardButton("🌐 Web-sayt (Full-stack)"))
        kb.row(KeyboardButton("🛠 Texnik yordam / Boshqa"))
        bot.send_message(chat_id, "📁 <b>Sizga qanday turdagi loyiha kerak?</b>", reply_markup=kb)
        
    elif state['step'] == 'project_type':
        state['project_type'] = message.text
        state['step'] = 'details'
        hide_kb = telebot.types.ReplyKeyboardRemove()
        bot.send_message(chat_id, "💬 <b>Loyiha haqida qisqacha ma'lumot bering:</b> (nimalar qila olsin?)", reply_markup=hide_kb)
        
    elif state['step'] == 'details':
        state['details'] = message.text
        
        bot.send_message(chat_id, "<b>🎉 Rahmat! Buyurtmangiz qabul qilindi. Tez orada siz bilan aloqaga chiqaman!</b>", reply_markup=main_menu())
        
        client_username = f"@{message.from_user.username}" if message.from_user.username else "Yashirin"
        report = (
            f"<b>🚨 YANGI MIJOZ VA BUYURTMA!</b>\n\n"
            f"👤 <b>Ismi:</b> {state['name']}\n"
            f"📞 <b>Tel:</b> {state['phone']}\n"
            f"🛠 <b>Loyiha turi:</b> {state['project_type']}\n"
            f"📝 <b>Tavsif:</b> {state['details']}\n\n"
            f"🔗 <b>Mijoz profili:</b> {client_username}"
        )
        try:
            bot.send_message(ADMIN_ID, report)
        except Exception as e:
            print(f"Admin xabar xatosi: {e}")
            
        user_states.pop(chat_id)

if __name__ == '__main__':
    print("F1 Portfolio + Business boti muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling()