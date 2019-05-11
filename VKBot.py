import requests
import random
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


print(send_msg_to_user(61118227, str(random.random()*1000)))
# print(send_msg_to_chat(200, str(random.random()*1000)))