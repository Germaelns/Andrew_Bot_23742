from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, VARCHAR, PrimaryKeyConstraint, UniqueConstraint

Base = declarative_base()


class Group(Base):
    __tablename__ = 'group'

    id = Column('id', INTEGER, autoincrement=True)
    group_id = Column('group_id', INTEGER, nullable=False)

    PrimaryKeyConstraint(id, name='PK_Group_Id')
    UniqueConstraint(group_id, name="UQ_Group_group_id")


class Link(Base):
    __tablename__ = 'link'

    id = Column('id', INTEGER, autoincrement=True)
    image = Column('image', VARCHAR(1000), nullable=False)
    title = Column('title', VARCHAR(1000), nullable=False)
    url = Column('url', VARCHAR(1000), nullable=False)

    PrimaryKeyConstraint(id, name="PK_Link_Id")
    UniqueConstraint(url, name="UQ_Link_Url")


class Variable(Base):
    __tablename__ = 'variable'

    id = Column('id', INTEGER, autoincrement=True)
    value = Column('value', VARCHAR(200), nullable=False)
    description = Column('description', VARCHAR(200), nullable=False)

    PrimaryKeyConstraint(id, name="PK_Variable_Id")
    UniqueConstraint(description, name="UQ_Variable_Description")


if __name__ == '__main__':

    from sqlalchemy import create_engine
    from config import POSTGRE_URI
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(POSTGRE_URI)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    session.add(Variable(value="1a36c8564ba171614dcf", description="access_token"))
    session.add(Variable(value="0", description="refresh_token"))
    session.add(Variable(value="9", description="start_timer"))
    session.add(Variable(value="21", description="end_timer"))
    session.add(Variable(value="0", description="last_post_time"))
    session.add(Variable(value="754428059:AAFYwBQYdp2k2K1TRQcFCnZIJ3RKmk1pOng", description="telegram_bot_token"))
    session.add(Variable(value="@trash7289563405", description="chat_id"))
    session.add(Variable(value="b42f8401b42f8401b42f8401e0b44504ebbb42fb42f8401e8f91a4da1bad7811ea125e6", description="vk_app_token"))

    session.commit()
    session.close()


