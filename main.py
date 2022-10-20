# task1


import psycopg2
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale


DSN = 'postgresql://postgres:rusarm77@localhost:5432/bookshop_db'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# task3


with open('data.json', 'r') as fd:
    data = json.load(fd)
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))

session.commit()
session.close()


# task2


def conn_any_db():
    try:
        db_type = input('Введите тип БД, к которому желаете подключиться: ')
        username = input('Введите имя пользователя: ')
        password = input('Введите пароль: ')
        hostname = input('Введите имя хоста: ')
        code = input('Введите код: ')
        db_name = input('Введите название БД: ')
        connection = f'{db_type}://{username}:{password}@{hostname}:{code}/{db_name}'
        DSN = connection
        connect = sqlalchemy.create_engine(DSN)
    except:
        print('SMTH WENT WRONG...try again')
    else:
        print('Connected with DB! Everything is ok!')
    return connect


# * conn_any_db()
# Насчет этой функции, хотел у Вас уточнить как ее оптимизировать, чтобы при подключении к несуществующей БД срабатывал
# --> блок except? *


def find_shop(conn):
    publisher_name = input("What is publisher's name? ")
    with conn.cursor() as cur:
        cur.execute('''
            SELECT shop.name FROM shop
            JOIN stock ON stock.id_shop = shop.id
            JOIN book ON stock.id_book = book.id
            JOIN publisher ON book.id_publisher = publisher.id
            WHERE publisher.name=%s; 
            ''', (publisher_name,))
        print(cur.fetchone())


with psycopg2.connect(database="bookshop_db", user="postgres", password="rusarm77") as conn:
    find_shop(conn)









