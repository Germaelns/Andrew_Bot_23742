import requests
import re
import telebot
import vk
import time
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, VK_APP_TOKEN
from dal import BotDatabaseController


def get_url_from_vk_group(vk_groups):
    session = vk.Session(access_token=VK_APP_TOKEN)
    api = vk.API(session)

    urls = list()

    last_post_timing = 0

    for group in vk_groups:
        response = api.wall.get(owner_id=group, v=5.74, count=5)

        for item in response['items']:
            if last_post_timing < item['date']:
                if item['text'] is not "":
                    urls.append(re.search("(?P<url>https?://[^\s]+)", item["text"]).group("url"))
            else:
                print("Been before")

    last_post_timing = time.time()

    print(last_post_timing)
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

    print(access_token)

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "authorization": "Bearer " + access_token + ""
    }

    responce = requests.get('https://api.admitad.com/deeplink/911806/advcampaign/6115/?ulp=' + url, headers=headers)

    print(responce.json())

    return responce.json()[0]


def post_to_telegram(image, title, url):
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=image, caption="{0}\n\n{1}".format(title, url))


if __name__ == "__main__":

    urls = get_url_from_vk_group()

    for url in urls:
        try:
            info = get_info_from_url(url)
            post_to_telegram(image=info[0][0], title=info[1][0], url=create_deeplinks(info[2]))
        except:
            pass



