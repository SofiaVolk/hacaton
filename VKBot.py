import requests
import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

TOKEN = "bafa83804e118b05e67670d10ac9993b98369fb6129c353e85efef71dfa0070bf43b3d2b551ed67d9d0e8"  # for hakaton
url = "https://api.vk.com/method/"


def send_message(func):
    def wrapper(id, text):
        params = func(id, text)
        response = requests.post(url + "messages.send", params=params).json()
        return response
    return wrapper


@send_message
def send_msg_to_chat(id, text):
    params = {"chat_id": id, "message": text, "random_id": 0, "access_token": TOKEN, "v": 5.95}
    return params


@send_message
def send_msg_to_user(id, text):
    params = {"user_ids": id, "message": text, "random_id": 0, "access_token": TOKEN, "v": 5.95}
    return params


def chat_info(id):
    params = {"chat_id": id, "access_token": TOKEN, "v": 5.95}
    response = requests.post(url + "messages.getChat", params=params).json()
    print(response)


# print(send_msg_to_user(61118227, str(random.random()*1000)))

vk_session = vk_api.VkApi(token='токен с доступом к сообщениям и фото')
longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
    # Слушаем longpoll, если пришло сообщение то:
        print(send_msg_to_user(event.user_id, message="ПРИВЕТ :3"))

    #     if event.text == 'Первый вариант фразы' or event.text == 'Второй вариант фразы': #Если написали заданную фразу
    #         if event.from_user: #Если написали в ЛС
    #             # Отправляем сообщение
    #             vk.messages.send(user_id=event.user_id, message='Ваш текст')
    #         elif event.from_chat: #Если написали в Беседе
    #             # Отправляем собщение
    #             vk.messages.send( chat_id=event.chat_id, message='Ваш текст')