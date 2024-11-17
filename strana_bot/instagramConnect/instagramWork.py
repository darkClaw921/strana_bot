from instabot import Bot
import time
import schedule
#https://developers.facebook.com/docs/messenger-platform/get-started/
#https://developers.facebook.com/docs/messenger-platform/webhooks
#https://developers.facebook.com/docs/messenger-platform/instagram
#https://developers.facebook.com/docs/messenger-platform/instagram/sample-experience  
# Настройка и логин в Instagram
bot = Bot(like_delay=60)
bot.login(username="", password="")

# Функция обработки сообщений
def process_message(message):
    # Обрабатывайте сообщение здесь, как вам нужно
    response = f"Ваше сообщение: {message}"
    return response

# Функция проверки новых сообщений и отправки ответов
def check_messages():
    inbox = bot.get_messages()
    for message in inbox['messages']:
        if message['status'] == 'unread':
            user_id = message['user_id']
            user_message = message['text']
            response = process_message(user_message)
            bot.send_message(response, [user_id])

# Планирование регулярной проверки сообщений
schedule.every(1).minutes.do(check_messages)

while True:
    schedule.run_pending()
    time.sleep(1)