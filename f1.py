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
        time.sleep(600)  # Har 10 daqiqada tarmoqni tekshiradi

threading.Thread(target=keep_alive, daemon=True).start()

# =====================================================================
# ⚙️ BOT SOZLAMALARI VA TOKENLAR
# =====================================================================
API_TOKEN = '8877192617:AAGKNS5OJoPtdO3f8uZawoHLt1s07G-1Gd0'
ADMIN_ID = 8608832630  # Sening shaxsiy ID'ing (Faqat senga javob bermasligi uchun)

bot = telebot.TeleBot(API_TOKEN, parse_mode='HTML')

# Foydalanuvchilar holati (Buyurtma tizimi va aqlli cheklov uchun)
user_states = {}
replied_users = {}  # {user_id: oxirgi_javob_vaqti}

# 🌟 Jozibali va Premium Ko'rinishdagi Asosiy Menyu
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
# ⚡️ AQLLI KOTIB REJIMI: SHAXSIY PROFIL UCHUN JAVOBLAR (SPAMSIZ)
# =====================================================================
@bot.business_message_handler(func=lambda message: True)
def handle_business_message(message):
    """ Profilingizga xabar kelganda faqat mijozga/do'stga 24 soatda bir marta ajoyib javob beradi """
    chat_id = message.chat.id
    user_id = message.from_user.id
    business_connection_id = message.business_connection_id
    user_name = message.from_user.first_name
    current_time = time.time()

    # 1. AGAR O'ZINGIZ PROFIYINGIZDAN KIMGAdir YOZAYOTGAN BO'LSANGIZ, BOT MUTLAQO JIM TURADI
    if user_id == ADMIN_ID:
        return

    # 2. AQLLI VAQTIY CHEKLOV: Bitta odamga har 24 soatda faqat 1 marta javob qaytaradi
    if user_id in replied_users:
        last_replied_time = replied_users[user_id]
        if current_time - last_replied_time < 86400:  # 86400 soniya = 24 soat
            return

    # 3. YANAYAM AJOYIBROQ VA PREMIUM AVTO-JAVOB MATNI
    auto_text = (
        f"<b>👋 Salom, {user_name}! Kuningiz xayrli va unumli o'tsin!</b>\n\n"
        f"Hozircha @RnFlexx biroz band yoki muhim kod ustida ishlamoqda. 💻✨\n"
        f"Men uning shaxsiy raqamli yordamchisiman va sizning xabaringizni xavfsiz qabul qildim! 🤖\n\n"
        f"🧭 <b>Agar sizga:</b>\n"
        f"• Zamonaviy va tezkor Web-saytlar\n"
        f"• Murakkab va avtomatlashtirilgan Telegram botlar kerak bo'lsa:\n\n"
        f"Mening rasmiy botimga o'tib, portfoliosi va narxlar bilan tanishishingiz yoki to'g'ridan-to'g'ri buyurtma qoldirishingiz mumkin: @{bot.get_me().username}\n\n"
        f"<i>Xabaringiz unga yetkazildi, bo'shashi bilan shaxsan o'zi aloqaga chiqadi. Rahmat! 🙏</i>"
    )

    try:
        bot.send_message(
            chat_id=chat_id, 
            text=auto_text, 
            business_connection_id=business_connection_id
        )
        # Foydalanuvchini vaqtini saqlab qo'yamiz (bugun boshqa javob yozmaydi)
        replied_users[user_id] = current_time
    except Exception as e:
        print(f"Biznes xabar yuborishda xato: {e}")

# =====================================================================
# 🤖 BOTNING O'ZIGA KIRGAN FOYDALANUVCHILAR UCHUN INTERFEYS
# =====================================================================

# /start komandasi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id in user_states:
        user_states.pop(message.chat.id)
        
    welcome_text = (
        f"<b>🚀 Xush kelibsiz, {message.from_user.first_name}!</b>\n\n"
        f"Siz IT dunyosida kreativ yechimlar va yuqori sifatni qadrlaydigan Full-stack dasturchi — "
        f"<b>Azizbek Fayzullayevning (@RnFlexx)</b> rasmiy portfolio botiga kardingiz.\n\n"
        f"⚡️ Quyidagi tugmalar orqali mening raqamli dunyomga sho'ng'ishingiz, tayyorlagan real loyihalarimni ko'rishingiz yoki o'z biznesingiz uchun eng mukammal loyihani buyurtma qilishingiz mumkin!"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

# Inline tugmalar bosilganda (Callback)
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    code = call.data
    
    if code == 'back_to_menu':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="✨ <b>Asosiy bosh menyu. O'zingizga kerakli bo'limni tanlang:</b>", reply_markup=main_menu())
        
    elif code == 'my_projects':
        projects_text = (
            "<b>💻 MASHHUR VA REAL LOYIHALARIM:</b>\n\n"
            "🍏 <b>Olcha Cafe</b> — Kafe va restoranlar uchun maxsus, QR-menyu va buyurtmalarni boshqarish bo'yicha mukammal Full-stack veb-tizim.\n\n"
            "⚡️ <b>Sambu (Welixma)</b> — Yuqori tezlikda ishlovchi, zamonaviy va futuristik interfeysga ega bo'lgan maxsus platforma.\n\n"
            "<i>💡 Har bir loyihani hozirning o'zida jonli (Live) rejimda sinab ko'rishingiz mumkin:</i>"
        )
        proj_kb = InlineKeyboardMarkup(row_width=1)
        proj_kb.add(
            InlineKeyboardButton(text="🟢 Olcha Cafe Saytini Ko'rish", url="https://kazajonykk-del.github.io/olcha/"),
            InlineKeyboardButton(text="🟣 Sambu (Welixma) Saytini Ko'rish", url="https://welixma.vercel.app/"),
            InlineKeyboardButton(text="⬅️ Bosh Menyoga Qaytish", callback_data="back_to_menu")
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text=projects_text, reply_markup=proj_kb)
        
    elif code == 'my_socials':
        # FACHATO INSAGRAM VA GITHUB QOLDIRILDI, TELEGRAM KANAL O'CHIRILDI
        social_kb = InlineKeyboardMarkup(row_width=1)
        social_kb.add(
            InlineKeyboardButton(text="📸 Rasmiy Instagram Profilim", url="https://www.instagram.com/rn.flexx/"),
            InlineKeyboardButton(text="💻 Professional GitHub Profilim", url="https://github.com/kazajonykk-del/"),
            InlineKeyboardButton(text="⬅️ Bosh Menyoga Qaytish", callback_data="back_to_menu")
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="<b>📱 Mening rasmiy internetdagi sahifalarim:</b>\n\nKuzatib borish va aloqaga chiqish uchun eng qulay yo'llar:", reply_markup=social_kb)
        
    elif code == 'my_location':
        loc_text = (
            "<b>📍 GEO-LOKATSIYA VA MANZIL:</b>\n\n"
            "O'zbekiston viloyati, Namangan, Chust tumani.\n\n"
            "🌍 <i>Masofaning ahamiyati yo'q! Butun dunyo bo'ylab istalgan davlat va shaharlar bilan online formatda shartnoma asosida ishonchli hamkorlik qilaman.</i>"
        )
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text="⬅️ Bosh Menyoga Qaytish", callback_data="back_to_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text=loc_text, reply_markup=kb)
        
    elif code == 'make_order':
        user_states[call.message.chat.id] = {'step': 'name'}
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="<b>🔥 Zo'r! Kelajakdagi loyihangizni birgalikda eng yuqori darajaga olib chiqamiz!</b>\n\nSiz bilan qanday bog'lansam bo'ladi? Ismingizni yozing:")

# Buyurtma berish so'rovnomasi (Step-by-Step)
@bot.message_handler(func=lambda message: message.chat.id in user_states)
def order_flow(message):
    chat_id = message.chat.id
    state = user_states[chat_id]
    
    if state['step'] == 'name':
        state['name'] = message.text
        state['step'] = 'phone'
        bot.send_message(chat_id, "<b>⚡️ Juda yaxshi!</b> Endi esa siz bilan bog'lanish uchun <b>Telefon raqamingizni</b> yozib qoldiring:")
        
    elif state['step'] == 'phone':
        state['phone'] = message.text
        state['step'] = 'project_type'
        
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.row(KeyboardButton("🤖 Avtomatlashtirilgan Telegram Bot"), KeyboardButton("🌐 Zamonaviy Web-sayt (Full-stack)"))
        kb.row(KeyboardButton("🛠 Mavjud loyihani sozlash / Boshqa masalalar"))
        bot.send_message(chat_id, "📁 <b>Biznesingiz yoki o'zingiz uchun qanday turdagi raqamli yechim kerak?</b>", reply_markup=kb)
        
    elif state['step'] == 'project_type':
        state['project_type'] = message.text
        state['step'] = 'details'
        hide_kb = telebot.types.ReplyKeyboardRemove()
        bot.send_message(chat_id, "💬 <b>Loyiha haqida batafsilroq ma'lumot bering:</b>\n\n(Dastur qanday vazifalarni bajarsin, qanday funksiyalari bo'lishi kerak?)", reply_markup=hide_kb)
        
    elif state['step'] == 'details':
        state['details'] = message.text
        
        bot.send_message(chat_id, "<b>🎉 Katta rahmat! Barcha ma'lumotlar qabul qilindi. Tez orada loyihangizni muhokama qilish uchun siz bilan shaxsan bog'lanaman!</b>", reply_markup=main_menu())
        
        client_username = f"@{message.from_user.username}" if message.from_user.username else "Yashirin Profil"
        report = (
            f"<b>🚨 YANGI PREMIUM BUYURTMA KELDI!</b>\n\n"
            f"👤 <b>Mijoz:</b> {state['name']}\n"
            f"📞 <b>Aloqa raqami:</b> {state['phone']}\n"
            f"🛠 <b>Yo'nalish:</b> {state['project_type']}\n"
            f"📝 <b>Loyiha g'oyasi:</b> {state['details']}\n\n"
            f"🔗 <b>Telegram profili:</b> {client_username}"
        )
        try:
            bot.send_message(ADMIN_ID, report)
        except Exception as e:
            print(f"Admin xabar xatosi: {e}")
            
        user_states.pop(chat_id)

if __name__ == '__main__':
    print("F1 Portfolio + Business boti yangilangan ko'rinishda muvaffaqiyatli ishlamoqda...")
    bot.infinity_polling()