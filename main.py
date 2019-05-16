import datetime

from bll import *

bot = telebot.TeleBot(TELEGRAM_TOKEN)

start_time = 9
end_time = 21
sleep_time = 900
vk_groups = [-87389803]


@bot.message_handler(commands=['start'])
def main(message):
    while True:

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
                        # post_to_telegram(image=info[0][0], title=info[1][0], url=create_deeplinks(info[2]))
                    except Exception as e:
                        print(e)

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
