# -*- coding: utf-8 -*-
import sqlalchemy.orm

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    addresses = relationship('Address', uselist=True, lazy='joined')

    def __init__(self, name, username):
        self.name = name
        self.username = username


class Address(Base):
    __tablename__ = 'user_address'
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, address, user_id):
        self.address = address
        self.user_id = user_id


if __name__ == "__main__":
    # engine = create_engine('sqlite:///:memory:', echo=True)
    engine = create_engine(
        'postgresql://root:root@192.168.2.42:27016/lazy_test', echo=True)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    # 設定有兩個user
    session.execute('TRUNCATE "user" CASCADE;')
    user1 = User('Jeff', 'jeff1111')
    session.add(user1)
    user2 = User('david', 'david1111')
    session.add(user2)
    session.flush()
    # print("transaction ID: ", session.execute("SELECT txid_current()").first())
    # 故意設定每個user有10筆Address table的資料
    for i in range(10):
        address = Address('Jeff address', user1.id)
        session.add(address)
        address = Address('david address', user2.id)
        session.add(address)
    session.commit()

    print("-"*100)
    users = session.query(User).all()
    print("-"*100)
    for user in users:
        print("1. get user.address")
        print(user.addresses)
        print("-"*100)
        print("2. get user.address")
        print(user.addresses)
        print("-"*100)
    # print("transaction ID: ", session.execute(
    #     "SELECT txid_current()").first())

# ----------------------------------------------------------------------------------------------------
# BEGIN(implicit)
# SELECT anon_1.user_id AS anon_1_user_id, anon_1.user_name AS anon_1_user_name, anon_1.user_username AS anon_1_user_username, user_address_1.id AS user_address_1_id, user_address_1.address AS user_address_1_address, user_address_1.user_id AS user_address_1_user_id
# FROM(SELECT user.id AS user_id, user.name AS user_name, user.username AS user_username
#      FROM user
#      LIMIT ? OFFSET ?) AS anon_1 LEFT OUTER JOIN user_address AS user_address_1 ON anon_1.user_id = user_address_1.user_id
# (1, 0)
# ----------------------------------------------------------------------------------------------------
# [ < __main__.Address object at 0x7f1eef38c790 > , < __main__.Address object at 0x7f1eef38c820 > , < __main__.Address object at 0x7f1eef38c880 > , < __main__.Address object at 0x7f1eef38c8e0 > , < __main__.Address object at 0x7f1eef38c940 > , < __main__.Address object at 0x7f1eef38c9a0 > , < __main__.Address object at 0x7f1eef38ca00 > , < __main__.Address object at 0x7f1eef38ca60 > , < __main__.Address object at 0x7f1eef38cac0 > , < __main__.Address object at 0x7f1eef3d6100 > ]
# ----------------------------------------------------------------------------------------------------
# [ < __main__.Address object at 0x7f1eef38c790 > , < __main__.Address object at 0x7f1eef38c820 > , < __main__.Address object at 0x7f1eef38c880 > , < __main__.Address object at 0x7f1eef38c8e0 > , < __main__.Address object at 0x7f1eef38c940 > , < __main__.Address object at 0x7f1eef38c9a0 > , < __main__.Address object at 0x7f1eef38ca00 > , < __main__.Address object at 0x7f1eef38ca60 > , < __main__.Address object at 0x7f1eef38cac0 > , < __main__.Address object at 0x7f1eef3d6100 > ]
# ----------------------------------------------------------------------------------------------------
