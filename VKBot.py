import vk_api
import time
from vk_api.longpoll import VkLongPoll, VkEventType
import logger
import word_analyzer as wa
from bot import ret_news

TOKEN = "bafa83804e118b05e67670d10ac9993b98369fb6129c353e85efef71dfa0070bf43b3d2b551ed67d9d0e8"  # for hakaton

bot_activation = False
vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()

initial_time = time.time()
logproc = logger.Logproc()
logproc.start()


def activating_bot(event, continue_status):
    status = bot_activation
    if "/start" in event.text.lower():
        msg = '''Привет, {}.\n
        Я умею находить новости по ключевым словам, которые ты напишешь. \n
        Если ты не хочешь увидеть новости про футбол или что-то еще, \n
        напиши --NEG: "то что не хочешь увидеть"
        '''.format(vk.users.get(user_id=event.user_id)[0]["first_name"])

        vk.messages.send(user_id=event.user_id, message=msg, random_id=0)
        status = True
        continue_status = True
    elif bot_activation and ("/stop" in event.text.lower()):
        msg = "Пока ✌️ Захочешь поболтать - пиши /start"
        vk.messages.send(user_id=event.user_id, message=msg, random_id=0)
        status = False
        continue_status = True
    return status, continue_status


def msg_limiter(msg):
    msg_limit = 3896
    if len(msg) > msg_limit:
        msg = msg[:msg_limit]
    return msg


prev_index = None
for event in longpoll.listen():
    continue_status = False
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        bot_activation, continue_status = activating_bot(event, continue_status)
        if continue_status:
            continue
        if bot_activation:
            logger.api_logger.info(f'{time.time() - initial_time},success')
            if (event.text.lower() == 'еще' or event.text.lower() == 'ещё') and prev_index:
                msg, prev_index = ret_news(index=prev_index)
                vk.messages.send(user_id=event.user_id, message=msg_limiter(msg), random_id=0)
                service_msg = "Введите Еще чтобы увидеть похожие"
                vk.messages.send(user_id=event.user_id, message=service_msg, random_id=0)
            else:
                msg, prev_index = wa.main(event.text)
                if event.from_user:
                    vk.messages.send(user_id=event.user_id, message=msg_limiter(msg), random_id=0)
                    if prev_index:
                        service_msg = "Введите 'Еще' чтобы увидеть похожие"
                        vk.messages.send(user_id=event.user_id, message=service_msg, random_id=0)
                elif event.from_chat:
                    vk.messages.send(chat_id=event.chat_id, message='Всем привет)')
        else:
            service_msg = "Введите /start, чтобы начать, и /stop, чтобы закончить"
            vk.messages.send(user_id=event.user_id, message=service_msg, random_id=0)
