import datetime

from bll import *

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import POSTGRE_URI
from dal import BotDatabaseController

bot = telebot.TeleBot(TELEGRAM_TOKEN)

some_engine = create_engine(POSTGRE_URI, pool_pre_ping=True)

bot_status = 0


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите ключ доступа для входа или exit для выхода"), get_password)


def get_password(message):
    if message.text == "bkng3g6n2hk6hmk2l2h5kj2h5jk26mlk2;h,436h26m4h23l,":
        bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите цифру в соответствии с "
                                                                              "необходимой операцией:\n1) Запустить "
                                                                              "бот\n2) Добавить группу\n3) Удалить "
                                                                              "группу\n4) Изменить время работы\n"
                                                                              "5) Изменить периодичность выхода постов "
                                                                              "\n6) Отобразить группы\n7) Завершить работу"), interface)
    else:
        bot.send_message(message.from_user.id, "Неверный ключ доступа")


def interface(message):
    if message.text == '1':
        global bot_status
        if bot_status == 0:
            bot.send_message(message.from_user.id, "Бот начал работу!")
            bot_status = 1
            start_bot()
            bot_status = 0
        else:
            bot.send_message(message.from_user.id, "Бот уже запущен!")
    elif message.text == '2':
        bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите ID группы вконтакте С МИНУСОМ\nПример: (-8562496)\n\n Либо выберите одну из операций ниже:\n1) Вернуться в меню\n2) Завершить работу "), interface_add_group)

    elif message.text == '3':
        bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите ID группы вконтакте С МИНУСОМ\nПример: (-8562496)\n\n Либо выберите одну из операций ниже:\n1) Вернуться в меню\n2) Завершить работу "), interface_delete_group)

    elif message.text == '4':
        bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите начало и конец времени работы через двуеточие\n Например: 9:21\n\n Либо выберите одну из операций ниже:\n1) Вернуться в меню\n2) Завершить работу"), interface_change_timing)

    elif message.text == '5':
        bot.register_next_step_handler(bot.send_message(message.from_user.id, "Выберите частоту загрузки постов: \n1) Каждые 15 мин\n2) Каждые 30 мин\n3) Каждые 45 мин\n4) Каждый час\n5) Каждые 2 часа\n6) Вернуться в меню \n 7) Завершить работу"), interface_change_iter_time)

    elif message.text == '6':

        interfaceSession = sessionmaker(bind=some_engine)
        interface_session = interfaceSession()

        groups = BotDatabaseController.get_all_vk_groups(interface_session)

        info_group = ""

        if groups:
            for group in groups:
                info_group = info_group + str(group) + "\n"
            bot.send_message(message.from_user.id, info_group)
            bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите цифру в соответствии с "
                                                                                  "необходимой операцией:\n1) Запустить "
                                                                                  "бот\n2) Добавить группу\n3) Удалить "
                                                                                  "группу\n4) Изменить время работы\n"
                                                                                  "5) Изменить периодичность выхода постов "
                                                                                  "\n6) Отобразить группы\n7) Завершить работу"),
                                           interface)
        else:
            bot.send_message(message.from_user.id, "Нет подключенных групп")
            bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите цифру в соответствии с "
                                                                                  "необходимой операцией:\n1) Запустить "
                                                                                  "бот\n2) Добавить группу\n3) Удалить "
                                                                                  "группу\n4) Изменить время работы\n"
                                                                                  "5) Изменить периодичность выхода постов "
                                                                                  "\n6) Отобразить группы\n7) Завершить работу"),
                                           interface)

        interface_session.commit()
        interface_session.close()

    elif message.text == '7':
        bot.send_message(message.from_user.id, "Прощайте, спасибо что обратились!")
    else:
        bot.send_message(message.from_user.id, "Команда выбрана неверно, прощайте")


def interface_add_group(message):

    if message.text == '1':
        bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите цифру в соответствии с "
                                                                              "необходимой операцией:\n1) Запустить "
                                                                              "бот\n2) Добавить группу\n3) Удалить "
                                                                              "группу\n4) Изменить время работы\n"
                                                                              "5) Изменить периодичность выхода постов "
                                                                              "\n6) Отобразить группы\n7) Завершить работу"),
                                       interface)
    elif message.text == '2':
        bot.send_message(message.from_user.id, "Прощайте, спасибо что обратились!")
    else:
        try:
            interfaceSession = sessionmaker(bind=some_engine)
            interface_session = interfaceSession()

            BotDatabaseController.add_vk_group(interface_session, int(message.text))

            interface_session.commit()
            interface_session.close()

            bot.send_message(message.from_user.id, "Группа успешно добавлена!")
            bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите цифру в соответствии с "
                                                                                  "необходимой операцией:\n1) Запустить "
                                                                                  "бот\n2) Добавить группу\n3) Удалить "
                                                                                  "группу\n4) Изменить время работы\n"
                                                                                  "5) Изменить периодичность выхода постов "
                                                                                  "\n6) Отобразить группы\n7) Завершить работу"),
                                           interface)
        except:
            bot.send_message(message.from_user.id, "Группа уже существует или введены некорректные данные")
            bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите цифру в соответствии с "
                                                                                  "необходимой операцией:\n1) Запустить "
                                                                                  "бот\n2) Добавить группу\n3) Удалить "
                                                                                  "группу\n4) Изменить время работы\n"
                                                                                  "5) Изменить периодичность выхода постов "
                                                                                  "\n6) Отобразить группы\n7) Завершить работу"),
                                           interface)


def interface_delete_group(message):

    if message.text == '1':
        bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите цифру в соответствии с "
                                                                              "необходимой операцией:\n1) Запустить "
                                                                              "бот\n2) Добавить группу\n3) Удалить "
                                                                              "группу\n4) Изменить время работы\n"
                                                                              "5) Изменить периодичность выхода постов "
                                                                              "\n6) Отобразить группы\n7) Завершить работу"),
                                       interface)
    elif message.text == '2':
        bot.send_message(message.from_user.id, "Прощайте, спасибо что обратились!")
    else:
        try:
            interfaceSession = sessionmaker(bind=some_engine)
            interface_session = interfaceSession()

            BotDatabaseController.delete_vk_group(interface_session, int(message.text))

            interface_session.commit()
            interface_session.close()

            bot.send_message(message.from_user.id, "Группа успешно удалена!")
            bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите цифру в соответствии с "
                                                                                  "необходимой операцией:\n1) Запустить "
                                                                                  "бот\n2) Добавить группу\n3) Удалить "
                                                                                  "группу\n4) Изменить время работы\n"
                                                                                  "5) Изменить периодичность выхода постов "
                                                                                  "\n6) Отобразить группы\n7) Завершить работу"),
                                           interface)
        except:
            bot.send_message(message.from_user.id, "Группа не существует в базе")
            bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите цифру в соответствии с "
                                                                                  "необходимой операцией:\n1) Запустить "
                                                                                  "бот\n2) Добавить группу\n3) Удалить "
                                                                                  "группу\n4) Изменить время работы\n"
                                                                                  "5) Изменить периодичность выхода постов "
                                                                                  "\n6) Отобразить группы\n7) Завершить работу"),
                                           interface)


def interface_change_timing(message):

    if message.text == '1':
        bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите цифру в соответствии с "
                                                                              "необходимой операцией:\n1) Запустить "
                                                                              "бот\n2) Добавить группу\n3) Удалить "
                                                                              "группу\n4) Изменить время работы\n"
                                                                              "5) Изменить периодичность выхода постов "
                                                                              "\n6) Отобразить группы\n7) Завершить работу"),
                                       interface)
    elif message.text == '2':
        bot.send_message(message.from_user.id, "Прощайте, спасибо что обратились!")
    else:
        try:

            time = message.text.split(':')

            interfaceSession = sessionmaker(bind=some_engine)
            interface_session = interfaceSession()

            BotDatabaseController.change_post_timing(interface_session, time[0], time[1])

            interface_session.commit()
            interface_session.close()

            bot.send_message(message.from_user.id, "Время успешно изменено!")
            bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите цифру в соответствии с "
                                                                                  "необходимой операцией:\n1) Запустить "
                                                                                  "бот\n2) Добавить группу\n3) Удалить "
                                                                                  "группу\n4) Изменить время работы\n"
                                                                                  "5) Изменить периодичность выхода постов "
                                                                                  "\n6) Отобразить группы\n7) Завершить работу"),
                                           interface)
        except:
            bot.send_message(message.from_user.id, "Введеные некорректные данные")
            bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите цифру в соответствии с "
                                                                                  "необходимой операцией:\n1) Запустить "
                                                                                  "бот\n2) Добавить группу\n3) Удалить "
                                                                                  "группу\n4) Изменить время работы\n"
                                                                                  "5) Изменить периодичность выхода постов "
                                                                                  "\n6) Отобразить группы\n7) Завершить работу"),
                                           interface)


def interface_change_iter_time(message):
    if message.text == '1' or message.text == '2' or message.text == '3' or message.text == '4' or message.text == '5':
        try:

            interfaceSession = sessionmaker(bind=some_engine)
            interface_session = interfaceSession()

            if message.text == '5':
                BotDatabaseController.change_post_iter_time(interface_session, '8')
            else:
                BotDatabaseController.change_post_iter_time(interface_session, message.text)

            interface_session.commit()
            interface_session.close()

            bot.send_message(message.from_user.id, "Время выхода постов успешно изменено!")
            bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите цифру в соответствии с "
                                                                                  "необходимой операцией:\n1) Запустить "
                                                                                  "бот\n2) Добавить группу\n3) Удалить "
                                                                                  "группу\n4) Изменить время работы\n"
                                                                                  "5) Изменить периодичность выхода постов "
                                                                                  "\n6) Отобразить группы\n7) Завершить работу"),
                                           interface)
        except:
            pass
    elif message.text == '6':
        bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите цифру в соответствии с "
                                                                              "необходимой операцией:\n1) Запустить "
                                                                              "бот\n2) Добавить группу\n3) Удалить "
                                                                              "группу\n4) Изменить время работы\n"
                                                                              "5) Изменить периодичность выхода постов "
                                                                              "\n6) Отобразить группы\n7) Завершить работу"),
                                       interface)
    elif message.text == '7':
        bot.send_message(message.from_user.id, "Прощайте, спасибо что обратились!")
    else:
        bot.send_message(message.from_user.id, "Команда выбрана неверно, прощайте")


def start_bot():

    timer = 0

    while True:

        post_iter_time = time.time()

        Session = sessionmaker(bind=some_engine)
        session = Session()

        vk_groups = BotDatabaseController.get_all_vk_groups(session)
        start_time = int(BotDatabaseController.get_start_timer(session))
        end_time = int(BotDatabaseController.get_end_timer(session))
        sleep_time = int(BotDatabaseController.get_post_iter_time(session))

        hour = int(str(datetime.datetime.now().time())[:2]) + 3

        if hour == 24:
            hour = 0
        elif hour == 25:
            hour = 1
        elif hour == 26:
            hour = 2

        try:

            posts = get_url_from_vk_group(session, vk_groups)

            if not posts:
                pass
            else:
                for post in posts:
                    try:
                        info = get_info_from_url(post[1])
                        if 'aliexpress.com' in info[2]:
                            deeplink = create_deeplink(session, info[2])
                            BotDatabaseController.add_deeplink(session, image=info[0][0], title=post[0],
                                                               url=deeplink)
                    except:
                        pass

            session.commit()
            session.close()
            print("Done update")
        except:
            pass
        timer += 1

        if start_time <= hour < end_time and timer >= sleep_time:

            # post_engine = create_engine(POSTGRE_URI, pool_pre_ping=True)
            postSession = sessionmaker(bind=some_engine)
            post_session = postSession()

            try:
                url = BotDatabaseController.get_all_deeplinks(post_session)[-1]

                if url:
                    try:
                        post_to_telegram(url[0], url[1], url[2])
                        BotDatabaseController.delete_deeplink(post_session, url[2])
                    except Exception:
                        BotDatabaseController.delete_deeplink(post_session, url[2])
            except:
                pass

            post_session.commit()
            post_session.close()
            timer = 0
            print("Done post")

        if hour == 1:

            deleteSession = sessionmaker(bind=some_engine)
            delete_session = deleteSession()

            urls = BotDatabaseController.get_all_deeplinks(delete_session)

            if urls:
                for url in urls:
                    try:
                        BotDatabaseController.delete_deeplink(delete_session, url[2])
                    except:
                        pass

            delete_session.commit()
            delete_session.close()

        time.sleep(900 - (int(time.time()) - int(post_iter_time)))


bot.polling()

if __name__ == '__main__':

    start_bot()
