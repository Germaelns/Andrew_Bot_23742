from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, VARCHAR, PrimaryKeyConstraint

Base = declarative_base()


class Group(Base):
    __tablename__ = 'group'

    id = Column('id', INTEGER, autoincrement=True)
    vk_group_id = Column('group_id', int, nullable=False)

    PrimaryKeyConstraint(id, name='PK_Group_Id')


class Link(Base):
    __tablename__ = 'link'

    id = Column('id', INTEGER, autoincrement=True)
    image = Column('image', VARCHAR(1000), nullable=False)
    title = Column('title', VARCHAR(1000), nullable=False)
    url = Column('url', VARCHAR(1000), nullable=False)

    PrimaryKeyConstraint(id, name="PK_Link_Id")


class Variable(Base):
    __tablename__ = 'Variable'

    id = Column('id', INTEGER, autoincrement=True)
    value = Column('name', VARCHAR(30), nullable=False)
    description = Column('name', VARCHAR(30), nullable=False)

    PrimaryKeyConstraint(id, name="PK_Variable_Id")


if __name__ == '__main__':

    from sqlalchemy import create_engine

    engine = create_engine()
    Base.metadata.create_all(bind=engine)
