import requests
import models


class BotDatabaseController:
    @staticmethod
    def add_deeplink(session, image: str, title: str, url: str):
        return session.add(models.Link(image= image, title= title, url= url))

    @staticmethod
    def get_all_deeplinks(session) -> list:
        return list(map(lambda x: [x.image, x.title, x.url], session.query(models.Link).all()))

    @staticmethod
    def delete_deeplink(session, url: str):
        return session.query(models.Link).filter(models.Link.url == url).delete()

    @staticmethod
    def create_new_access_token(session):
        headers = {
             "content-type": "application/x-www-form-urlencoded",
             "authorization": "Basic ZjhjZmIzOTg5NGM4OGE1YmQzMzcyMzllM2U5YmQyOjQ0ODkwYTlmMjBhZDQzYjc3MTc5Y2M5ODc2YWNjMA=="
         }

        responce = requests.get('https://api.admitad.com/token?grant_type=client_credentials&client_id=f8cfb39894c88a5bd337239e3e9bd2&scope=deeplink_generator websites advcampaigns', headers=headers)
        session.query(models.Variable).filter(models.Variable.description == "access_token").update({'value': responce.json()['access_token']})

        return 0

    @staticmethod
    def get_access_token(session) -> str:
        return session.query(models.Variable).filter(models.Variable.description == "access_token").all()[0].value

    @staticmethod
    def add_vk_group(group_id: int, session):
        session.add(models.Group(group_id= group_id))

    @staticmethod
    def get_all_vk_groups(session) -> list:
        return list(map(lambda x: x.group_id, session.query(models.Group).all()))

    @staticmethod
    def delete_vk_group(group_id: int, session):
        return session.query(models.Group).filter(models.Group.group_id == group_id).delete()

    @staticmethod
    def change_post_timing(start: str, end: str):
        session.query(models.Variable).filter(models.Variable.description == "start_timer").update({'value': start})
        session.query(models.Variable).filter(models.Variable.description == "end_timer").update({'value': end})

    @staticmethod
    def change_last_post_time(time: str):
        session.query(models.Variable).filter(models.Variable.description == "last_post_time").update({'value': time})

    @staticmethod
    def change_check_timing(minutes):
        pass


if __name__ == "__main__":

    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    from config import POSTGRE_URI

    some_engine = create_engine(POSTGRE_URI)

    Session = sessionmaker(bind=some_engine)
    session = Session()

    # BotDatabaseController.create_new_access_token(session)
    # BotDatabaseController.get_access_token(session)
    # BotDatabaseController.add_vk_group(2376383, session)
    # BotDatabaseController.delete_vk_group(2376383, session)
    # BotDatabaseController.get_vk_groups(session)
    # BotDatabaseController.change_post_timing("8", "20")
    # BotDatabaseController.get_all_deeplinks(session)
    # BotDatabaseController.delete_deeplink(session, 'url5')
    # BotDatabaseController.get_all_deeplinks(session)
    session.add(models.Variable(value='0', description="last_post_time"))
    BotDatabaseController.change_last_post_time("25")
    session.commit()
    session.close()
