import requests
import models


class BotDatabaseController:
    @staticmethod
    def add_deeplink(session, image: str, title: str, url: str):
        return session.add(models.Link(image=image, title=title, url=url))

    @staticmethod
    def get_all_deeplinks(session) -> list:
        return list(map(lambda x: [x.image, x.title, x.url], session.query(models.Link).all()))

    @staticmethod
    def delete_deeplink(session, url: str):
        return session.query(models.Link).filter(models.Link.url == url).delete()

    @staticmethod
    def update_access_token(session, token: str):
        return session.query(models.Variable).filter(models.Variable.description == "access_token").update(
            {'value': token})

    @staticmethod
    def update_refresh_token(session, refresh_token: str):
        return session.query(models.Variable).filter(models.Variable.description == "refresh_token").update(
            {'value': refresh_token})

    @staticmethod
    def get_access_token(session) -> str:
        return session.query(models.Variable).filter(models.Variable.description == "access_token").all()[0].value

    @staticmethod
    def get_refresh_token(session) -> str:
        return session.query(models.Variable).filter(models.Variable.description == "refresh_token").all()[0].value

    @staticmethod
    def add_vk_group(session, group_id: int):
        return session.add(models.Group(group_id=group_id))

    @staticmethod
    def get_all_vk_groups(session) -> list:
        return list(map(lambda x: x.group_id, session.query(models.Group).all()))

    @staticmethod
    def delete_vk_group(session, group_id: int):
        return session.query(models.Group).filter(models.Group.group_id == group_id).delete()

    @staticmethod
    def change_post_timing(session, start: str, end: str):
        session.query(models.Variable).filter(models.Variable.description == "start_timer").update({'value': start})
        session.query(models.Variable).filter(models.Variable.description == "end_timer").update({'value': end})

    @staticmethod
    def get_start_timer(session):
        return session.query(models.Variable).filter(models.Variable.description == "start_timer").all()[0].value

    @staticmethod
    def get_end_timer(session):
        return session.query(models.Variable).filter(models.Variable.description == "end_timer").all()[0].value

    @staticmethod
    def get_last_post_time(session) -> str:
        return session.query(models.Variable).filter(models.Variable.description == "last_post_time").all()[0].value

    @staticmethod
    def change_last_post_time(session, time: str):
        session.query(models.Variable).filter(models.Variable.description == "last_post_time").update({'value': time})

    @staticmethod
    def change_post_iter_time(session, minutes: str):
        session.query(models.Variable).filter(models.Variable.description == "update_iter_time").update({'value': minutes*60})

    @staticmethod
    def get_post_iter_time(session):
        return session.query(models.Variable).filter(models.Variable.description == "update_iter_time").all()[0].value


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
    # session.add(models.Variable(value='0', description="last_post_time"))
    # BotDatabaseController.change_last_post_time("25")
    # BotDatabaseController.get_start_timer(session)
    # BotDatabaseController.get_end_timer(session)
    # BotDatabaseController.get_all_deeplinks(session)

    session.commit()
    session.close()
