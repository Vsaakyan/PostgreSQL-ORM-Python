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


def find_publisher():
    name_publ = input("Введите имя автора) : ")
    for n in session.query(Publisher).filter(Publisher.name.like(name_publ)).all():
        return n


with psycopg2.connect(database="bookshop_db", user="postgres", password="rusarm77") as conn:
    find_shop(conn)
    









