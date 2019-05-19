import datetime

from bll import *

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import POSTGRE_URI
from dal import BotDatabaseController

bot = telebot.TeleBot(TELEGRAM_TOKEN)


sleep_time = 900


@bot.message_handler(commands=['start'])
def main(message):
    while True:

        some_engine = create_engine(POSTGRE_URI)

        Session = sessionmaker(bind=some_engine)
        session = Session()

        vk_groups = BotDatabaseController.get_all_vk_groups(session)
        start_time = int(BotDatabaseController.get_start_timer(session))
        end_time = int(BotDatabaseController.get_end_timer(session))

        urls = list()
        hour = int(str(datetime.datetime.now().time())[:2])

        if start_time < hour < end_time:

            urls = get_url_from_vk_group(vk_groups)

            if not urls:
                pass
            else:
                for url in urls:
                    try:
                        info = get_info_from_url(url)
                        deeplink = create_deeplink(session, info[2])
                        BotDatabaseController.add_deeplink(session, image=info[0][0], title=info[1][0], url=deeplink)
                        # post_to_telegram(image=info[0][0], title=info[1][0], url=create_deeplinks(info[2]))
                    except Exception as e:
                        print(e)
                        pass

        session.commit()
        session.close()
        print("Done")
        time.sleep(sleep_time)

    # bot_response = bot.send_message(message.from_user.id, "Для того чтобы общаться со мной, нужно ввести пароль.")
    # bot.register_next_step_handler(bot_response, get_password)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.register_next_step_handler(bot.send_message(message.from_user.id, "Привет, введите свой пароль"), get_password)


def get_password(message):
    print(message)
    bot.send_message(message.from_user.id, "Your password is " + message.text)


bot.polling()
