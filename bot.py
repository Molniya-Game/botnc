from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import time
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import pyowm
from datetime import datetime, timedelta
import random
import os

API = "6d00d1d4e704068d70191bad2673e0cc"
owm = pyowm.OWM(API, language='ru')

token_vk = os.environ.get('BOT_TOKEN')

vk = vk_api.VkApi(token=str(token_vk))

vk._auth_token()

vk.get_api()

longpoll = VkBotLongPoll(vk, 180514096)  # Здесь id группы

keyboard = VkKeyboard(one_time=True)

keyboard.add_button('🔥Канал Discord NC🔥', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('🔥Группа NC🔥', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('🥶Закрыть🥶', color=VkKeyboardColor.NEGATIVE)


def send_msg(peer_id, message):
    vk.method("messages.send", {"peer_id": peer_id, "message": message, "random_id": 0})


def show_name():
    return [row[0] for row in cursor.execute('SELECT admins FROM team')]

while True:
    for event in longpoll.listen():
        if event.type == VkBotEventType.WALL_POST_NEW:
            peer_id = 2000000002
            id = event.object.id
            vk.method("messages.send",
                      {"peer_id": peer_id, "message": "🔥Новая запись!🔥", "attachment": "wall-180514096_" + str(id),
                       "random_id": 0})
            print("Новая Запись!")
        if event.type == VkBotEventType.MESSAGE_NEW:
            peer_id = event.object.peer_id
            message = event.object.text
            body = event.object.text.lower()
            chat_id = event.chat_id
            now = datetime.now() + timedelta(hours=3)
            user_id = event.object.from_id
            user_attachments = event.object.attachments
            print("Текст сообщения: " + str(message))
            print("Отправлено от: " + str(peer_id))
            print("Вложение: " + str(user_attachments))
            print("Отправлено в: " + str(now))
            print("---------------------------------------")
            if body == "/info":
                vk.method("messages.send",
                          {"peer_id": peer_id, "message": "Выбирай ;)", "keyboard": keyboard.get_keyboard(),
                           "random_id": 0})
            elif body == "[club180514096|@nismo_777] 🔥канал discord nc🔥" or body == "[club180514096|•nismo corporation | game group] 🔥канал discord nc🔥":
                send_msg(peer_id, "Держи😊\nНе покажу)")
            elif body == "[club180514096|@nismo_777] 🔥группа nc🔥" or body == "[club180514096|•nismo corporation | game group] 🔥группа nc🔥":
                send_msg(peer_id, "Лови😊\nhttps://vk.com/nismo_777")
            elif body.split(' ')[0] == "дог" and body.split(' ')[1] == "погода" or body.split(' ')[0] == "/дог" and \
                    body.split(' ')[1] == "погода":
                try:
                    observation = owm.weather_at_place(body.split(' ')[2])
                    w = observation.get_weather()
                    temp = w.get_temperature(unit='celsius')['temp']
                    status = w.get_detailed_status()
                    speed = w.get_wind()['speed']
                    vlazhn = w.get_humidity()
                    atm = w.get_pressure()['press']
                    send_msg(peer_id,
                             message.split(' ')[2] + "\nТекущая дата: " + str(now) + "\nТекущая температура: " + str(
                                 temp) + "°C\nСтатус: " + status + "\nСкорость ветра: " + str(
                                 speed) + "\nВлажность: " + str(vlazhn) + "%\nДавление: " + str(atm) + " мм рт. ст.")
                except:
                    send_msg(peer_id, "Город не найден...")
            elif body.split(' ')[0] == "дог" and body.split(' ')[1] == "инфа" or body.split(' ')[0] == "/дог" and \
                    body.split(' ')[1] == "инфа":
                send_msg(peer_id, "Вероятно, это " + str(random.randint(0, 100)) + "%")
            elif body.split(' ')[0] == "дог" and body.split(' ')[1] == "-1":
                try:
                    try:
                        mi = body.split('|')[0]
                        mem_id = mi.split('d')[1]
                        vk.method("messages.removeChatUser", {"chat_id": str(chat_id), "member_id": mem_id})
                    except:
                        reply_id = event.object.reply_message['from_id']
                        vk.method("messages.removeChatUser", {"chat_id": str(chat_id), "member_id": str(reply_id)})
                except:
                    send_msg(peer_id, "Нельзя удалить из мультидиалога администратора...")
        time.sleep(3)
