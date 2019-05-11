import vk_api
import requests

from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token='токен с доступом к сообщениям и фото')
longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
    # Слушаем longpoll, если пришло сообщение то:
        if event.text == 'Первый вариант фразы' or event.text == 'Второй вариант фразы': #Если написали заданную фразу
            if event.from_user: #Если написали в ЛС
                # Отправляем сообщение
                vk.messages.send(user_id=event.user_id, message='Ваш текст')
            elif event.from_chat: #Если написали в Беседе
                # Отправляем собщение
                vk.messages.send( chat_id=event.chat_id, message='Ваш текст')