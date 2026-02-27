import telebot
import random
import os
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# ----- Заглушка для порта (чтобы Railway думал, что всё ок) -----
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running')
    def log_message(self, format, *args):
        pass  # не выводим логи запросов

def run_webserver():
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"Заглушка запущена на порту {port}")
    server.serve_forever()

# Запускаем сервер в отдельном потоке
threading.Thread(target=run_webserver, daemon=True).start()
# --------------------------------------------------------------

# Токен из переменных окружения Railway
TOKEN = os.environ.get('TELEGRAM_TOKEN')
if not TOKEN:
    print("ОШИБКА: TELEGRAM_TOKEN не найден!")
    exit(1)

bot = telebot.TeleBot(TOKEN)

# Твои любовные записки
messages = [
    "❤️ Я люблю тебя также сильно, как мы любим пить пиво в пятницу вечером",
    "🌸 Ты прекрасна, как первый весенний цветок",
    "💃 С тобой даже понедельник feels like пятница",
    "☕ Ты — мое утро, мой кофе и мое счастье",
    "💕 Спасибо, что ты есть. Каждый день спасибо",
    "😊 Ты — причина моей улыбки",
    "🎁 Ты — лучший подарок в моей жизни",
    "🌟 С тобой каждый день как праздник",
    "💝 Ты — самое лучшее, что со мной случилось",
    "🌈 Ты делаешь мой мир ярче"
]

@bot.message_handler(commands=['start'])
def start_message(message):
    user_name = message.from_user.first_name
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = telebot.types.KeyboardButton("💌 Скажи что-нибудь")
    markup.add(button)
    
    bot.send_message(
        message.chat.id,
        f"🌸 Привет, {user_name}!\n\n"
        "Этот бот создан специально для тебя. 💝\n"
        "Нажми на кнопку ниже, и я скажу тебе что-то очень важное.",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "💌 Скажи что-нибудь")
def send_love_message(message):
    love_message = random.choice(messages)
    bot.send_message(
        message.chat.id,
        f"✨ *Тебе записка:* ✨\n\n{love_message}",
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = telebot.types.KeyboardButton("💌 Скажи что-нибудь")
    markup.add(button)
    
    bot.send_message(
        message.chat.id,
        "Нажми на кнопку внизу, я хочу тебе что-то сказать 💌",
        reply_markup=markup
    )

print("✅ Бот запущен и готов работать 24/7!")

# Запуск бота с защитой от разрывов
while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
        continue