import time
import random
from pyrogram import Client, enums
from config import msg, chats


api_id = 123
api_hash = "hash"

# Настройки
MIN_DELAY = 7 #Минимальная задержка между отправкой сообщений
MAX_DELAY = 18 # Максимальная задержка между отправкой сообщений
TYPING_DELAY_MIN = 3 #Минимальное время имитации печати
TYPING_DELAY_MAX = 3 #Максимальное время имитации печати
ERROR_DELAY = 5 #Задержа на след. действие после какой-либо ошибки
STICKER_CHANCE = 0.0 #Шанс того, что бот отправит  стикер вместо сообщения (0.1 = 10%, 0.3 = 30%, 1 = 100%)  

app = Client("my_account", api_id, api_hash)

# ID Стикеров. Получить ID стикера - @LeadConverterToolkitBot
STICKERS = [
    "CAACAgIAAxkBAAEPhY1oOwj3pQZuHAUjo_FAKz_IAAFm9xoAAuMfAAKDONBLQ3X4TCM37yE2BA",  # Свинка 1 xd
    "CAACAgIAAxkBAAEPhY9oOwkO6KzTa2ZhXlIB9ZzKkwuFCAAC0G8AAs-z-Us7Iouq16hciTYE",  # Свинка 2 xd
]

def simulate_typing(chat_id):
    try:
        delay = random.uniform(TYPING_DELAY_MIN, TYPING_DELAY_MAX)
        app.send_chat_action(chat_id, enums.ChatAction.TYPING)
        time.sleep(delay)
    except Exception as e:
        print(f"Ошибка в simulate_typing: {e}")

def simulate_choosing_sticker(chat_id):
    try:
        # Имитация выбора стикера (2-4 секунды)
        delay = random.uniform(2, 4)
        app.send_chat_action(chat_id, enums.ChatAction.CHOOSE_STICKER)
        time.sleep(delay)
    except Exception as e:
        print(f"Ошибка при выборе стикера: {e}")

def get_message():
    if isinstance(msg, list):
        return random.choice(msg)
    return msg

def random_delay():
    delay = random.uniform(MIN_DELAY, MAX_DELAY)
    print(f"Случайная задержка {delay:.1f} сек...")
    time.sleep(delay)

app.start()

try:
    while True:
        random.shuffle(chats)
        
        for chat_id in chats:
            try:
                if random.random() < STICKER_CHANCE:
                    simulate_choosing_sticker(chat_id)
                    sticker = random.choice(STICKERS)
                    app.send_sticker(chat_id, sticker)
                    print(f"Отправлен стикер в {chat_id}")
                else:
                    simulate_typing(chat_id)
                    

                    if random.random() > 0.1:
                        app.send_message(
                            chat_id,
                            get_message(),
                            parse_mode=enums.ParseMode.MARKDOWN
                        )
                        print(f"Отправлено сообщение в {chat_id}")
                    else:
                        print(f"Пропуск отправки в {chat_id} (случайный выбор)")
                
                random_delay()
                    
            except Exception as e:
                print(f"Ошибка в чате {chat_id}: {e}")
                time.sleep(ERROR_DELAY)

        cycle_delay = random.uniform(5, 10) #Минимальное,макисмальное время задержки перед началом нового цикла
        print(f"НАчало нового цикла через {cycle_delay:.1f} сек...")
        time.sleep(cycle_delay)

except KeyboardInterrupt:
    print("Остановлено")
finally:
    app.stop()
