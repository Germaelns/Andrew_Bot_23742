import datetime

from bll import *

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import POSTGRE_URI
from dal import BotDatabaseController

bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите пароль или exit для выхода"), get_password)


def get_password(message):
    if message.text == "Password56734518":
        bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите цифру в соответствии с необходимой операцией:\n1) Запустить постинг на канал\n2) Запустить парсинг ВК\n3) Добавить группу\n4) Удалить группу\n5) Изменить промежутки времени постинга\n6) Изменить частоту постинга\n7) Выйти \n8) Выключить бота"), interface)
    elif message.text == "exit":
        bot.send_message(message.from_user.id, "Прощайте, спасибо что обратились!")
    else:
        bot.send_message(message.from_user.id, "Неверный пароль")


def interface(message):
    if message.text == '1':
        try:
            bot.send_message(message.from_user.id, "Бот начнёт постинг на канал после первого парсинга ВК!")
            post()
        except Exception as e:
            print(e)
            bot.send_message(message.from_user.id, "Упс, возникла ошибка")

    elif message.text == '2':
        try:
            bot.send_message(message.from_user.id, "Бот начал парсинг и работает!")
            update()
        except Exception as e:
            print(e)
            bot.send_message(message.from_user.id, "Упс, возникла ошибка")

    elif message.text == '3':
        bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите ID группы вконтакте С МИНУСОМ\n Пример: (-8562496)"), interface_add_group)
    elif message.text == '4':
        bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите ID группы вконтакте С МИНУСОМ\n Пример: (-8562496)"), interface_delete_group)
    elif message.text == '5':
        bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите начало и конец времени через двуеточие\n Например: 9:21"), interface_change_timing)
    elif message.text == '6':
        bot.register_next_step_handler(bot.send_message(message.from_user.id, "Введите частоту загрузки постов цифрой в минутах (минимум 30 минут)"), interface_delete_group)
    elif message.text == '7':
        bot.send_message(message.from_user.id, "Прощайте, спасибо что обратились!")
    elif message.text == '8':
        bot.send_message(message.from_user.id, "Бот прекращает свою работу")
        bot.stop_bot()


def interface_add_group(message):
    try:
        interface_engine = create_engine(POSTGRE_URI, pool_pre_ping=True)

        interfaceSession = sessionmaker(bind=interface_engine)
        interface_session = interfaceSession()

        BotDatabaseController.add_vk_group(interface_session, int(message.text))

        interface_session.commit()
        interface_session.close()

        bot.send_message(message.from_user.id, "Группа успешно добавлена!")
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, "Упс, возникла ошибка")


def interface_delete_group(message):
    try:
        interface_engine = create_engine(POSTGRE_URI, pool_pre_ping=True)

        interfaceSession = sessionmaker(bind=interface_engine)
        interface_session = interfaceSession()

        BotDatabaseController.delete_vk_group(interface_session, int(message.text))

        interface_session.commit()
        interface_session.close()

        bot.send_message(message.from_user.id, "Группа успешно удалена!")
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, "Упс, возникла ошибка")


def interface_change_timing(message):

    try:
        time = message.text.split(':')
        interface_engine = create_engine(POSTGRE_URI, pool_pre_ping=True)

        interfaceSession = sessionmaker(bind=interface_engine)
        interface_session = interfaceSession()

        BotDatabaseController.change_post_timing(interface_session, time[0], time[1])

        interface_session.commit()
        interface_session.close()

        bot.send_message(message.from_user.id, "Время успешно изменено!")
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, "Упс, возникла ошибка")


def interface_change_iter_time(message):
    try:
        interface_engine = create_engine(POSTGRE_URI, pool_pre_ping=True)

        interfaceSession = sessionmaker(bind=interface_engine)
        interface_session = interfaceSession()

        BotDatabaseController.change_post_iter_time(interface_session, message.text)

        interface_session.commit()
        interface_session.close()

        bot.send_message(message.from_user.id, "Время выхода постов успешно изменено!")
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, "Упс, возникла ошибка")


def update():
    print("hello")
    while True:

        update_iter_time = time.time()

        some_engine = create_engine(POSTGRE_URI, pool_pre_ping=True)

        Session = sessionmaker(bind=some_engine)
        session = Session()

        vk_groups = BotDatabaseController.get_all_vk_groups(session)
        start_time = int(BotDatabaseController.get_start_timer(session))
        end_time = int(BotDatabaseController.get_end_timer(session))
        # sleep_time = float(BotDatabaseController.get_post_iter_time(session))
        sleep_time = 60

        urls = list()
        hour = int(str(datetime.datetime.now().time())[:2])

        if start_time < hour < end_time:

            urls = get_url_from_vk_group(session, vk_groups)

            if not urls:
                pass
            else:
                for url in urls:
                    info = get_info_from_url(url)
                    if 'aliexpress.com' in info[2]:
                        deeplink = create_deeplink(session, info[2])
                        BotDatabaseController.add_deeplink(session, image=info[0][0], title=info[1][0], url=deeplink)
                    # post_to_telegram(image=info[0][0], title=info[1][0], url=create_deeplinks(info[2]))

        session.commit()
        session.close()
        print("Done")
        time.sleep(sleep_time - (time.time()-update_iter_time))


def post():

    while True:

        post_iter_time = time.time()

        post_engine = create_engine(POSTGRE_URI, pool_pre_ping=True)
        postSession = sessionmaker(bind=post_engine)
        post_session = postSession()

        urls = BotDatabaseController.get_all_deeplinks(post_session)

        for url in urls:
            try:
                post_to_telegram(url[0], url[1], url[2])
                BotDatabaseController.delete_deeplink(post_session, url[2])
            except Exception:
                pass

        post_session.commit()
        post_session.close()

        time.sleep(900 - (int(time.time())-int(post_iter_time)))


bot.polling()
