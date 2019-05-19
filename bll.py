import requests
import re
import telebot
import vk
import time
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, VK_APP_TOKEN
from dal import BotDatabaseController


def create_new_access_token(session):
    refresh_token = BotDatabaseController.get_refresh_token(session)

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "authorization": "Basic ZjhjZmIzOTg5NGM4OGE1YmQzMzcyMzllM2U5YmQyOjQ0ODkwYTlmMjBhZDQzYjc3MTc5Y2M5ODc2YWNjMA=="
    }

    responce = requests.get('https://api.admitad.com/token?grant_type=refresh_token&client_id'
                            '=f8cfb39894c88a5bd337239e3e9bd2&refresh_token='+ refresh_token
                            +'&client_secret=44890a9f20ad43b77179cc9876acc0', headers=headers)

    BotDatabaseController.update_access_token(session, responce.json()['access_token'])
    BotDatabaseController.update_refresh_token(session, responce.json()['refresh_token'])
    return 0


def get_url_from_vk_group(session_db, vk_groups):
    session = vk.Session(access_token=VK_APP_TOKEN)
    api = vk.API(session)

    urls = list()

    last_post_timing = float(BotDatabaseController.get_last_post_time(session_db))

    for group in vk_groups:
        response = api.wall.get(owner_id=group, v=5.74, count=5)

        for item in response['items']:
            if last_post_timing < item['date']:
                if item['text'] is not "":
                    urls.append(re.search("(?P<url>https?://[^\s]+)", item["text"]).group("url"))

    BotDatabaseController.change_last_post_time(session_db, str(time.time()))

    return urls


def get_info_from_url(url):
    response = requests.get(url)

    url = re.findall(r'<meta property="og:url" content=[\'"]?([^\'" >]+)', str(response.content))
    image = re.findall(r'<meta property="og:image" content=[\'"]?([^\'" >]+)', str(response.content))
    title = re.findall(r'<title[^>]*>([^<]+)</title>', str(response.content.decode(encoding='utf-8')))

    url = str(url).split('?', 2)[0].replace('[', '').replace("'", '')

    if "https:https:" in url:
        url = url.replace("https:https:", "https:")

    return [image, title, url]


def create_deeplink(session, url):

    access_token = BotDatabaseController.get_access_token(session)

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "authorization": "Bearer " + access_token + ""
    }

    responce = requests.get('https://api.admitad.com/deeplink/911806/advcampaign/6115/?ulp=' + url, headers=headers)

    if responce.status_code is not 200:
        create_new_access_token(session)

        responce = requests.get('https://api.admitad.com/deeplink/911806/advcampaign/6115/?ulp=' + url, headers=headers)

    return responce.json()[0]


def post_to_telegram(image, title, url):
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=image, caption="{0}\n\n{1}".format(title, url))


if __name__ == "__main__":

    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    from config import POSTGRE_URI

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



