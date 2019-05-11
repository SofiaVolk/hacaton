import requests
import random
import vk_api
import time
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import logger
import word_analyzer as wa

TOKEN = "bafa83804e118b05e67670d10ac9993b98369fb6129c353e85efef71dfa0070bf43b3d2b551ed67d9d0e8"  # for hakaton

bot_activation = False
vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()

initial_time = time.time()
logproc = logger.Logproc()
logproc.start()
answers = ["Твои шутки - отпад 🤣", "Я так рад тебя видеть 😍", "Блин, клево)",
                  "А расскажи еще что-нибудь", "Лол", "Ахахаха", "Ору 😅", "Го еграть? :3", "👍"]


def activating_bot(event):
    status = bot_activation
    if "/start" in event.text.lower():
        msg = "Привет, {}".format(vk.users.get(user_id=event.user_id)[0]["first_name"])
        vk.messages.send(user_id=event.user_id, message=msg, random_id=0)
        status = True
    elif bot_activation and ("/stop" in event.text.lower()):
        msg = "Пока ✌️ Захочешь поболтать - пиши /start"
        vk.messages.send(user_id=event.user_id, message=msg, random_id=0)
        status = False
    return status


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        bot_activation = activating_bot(event)
        if bot_activation:
            logger.api_logger.info(f'{time.time() - initial_time},success')
        # Слушаем longpoll, если пришло сообщение то:
            msg = wa.main(event.text)
            if event.from_user: #Если написали в ЛС
                # Отправляем сообщение
                msg = "Привет, {}".format(vk.users.get(user_id=event.user_id)[0]["first_name"])
                vk.messages.send(user_id=event.user_id, message=random.choice(answers), random_id=0)
            elif event.from_chat: #Если написали в Беседе
                # Отправляем собщение
                vk.messages.send(chat_id=event.chat_id, message='Всем привет)')
        else:
            service_msg = "Введите /start, чтобы начать, и /stop, чтобы закончить"
            vk.messages.send(user_id=event.user_id, message=service_msg, random_id=0)

