import sqlalchemy
import configparser
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale


config = configparser.ConfigParser()
config.read('settings.ini')
DSN = config['token']['dsn']

engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

pb1 = Publisher(name="OReilly")
pb2 = Publisher(name="Pearson")
pb3 = Publisher(name="Microsoft Press")
pb4 = Publisher(name="No starch press")

session.add_all([pb1, pb2, pb3, pb4])
session.commit()

b1 = Book(title="Programming Python, 4th Edition", publisher_id=1)
b2 = Book(title="Learning Python, 4th Edition", publisher_id=1)
b3 = Book(title="Natural Language Processing with Python", publisher_id=1)
b4 = Book(title="Hacking: The Art of Exploitation", publisher_id=4)
b5 = Book(title="Modern Operating Systems", publisher_id=2)
b6 = Book(title="Code Complete: Second Edition", publisher_id=3)

session.add_all([b1, b2, b3, b4, b5, b6])
session.commit()

sh1 = Shop(name="Labirint")
sh2 = Shop(name="OZON")
sh3 = Shop(name="Amazon")

session.add_all([sh1, sh2, sh3])
session.commit()

s1 = Stock(book_id=1, shop_id=1, count=34)
s2 = Stock(book_id=2, shop_id=1, count=30)
s3 = Stock(book_id=3, shop_id=1, count=0)
s4 = Stock(book_id=5, shop_id=2, count=40)
s5 = Stock(book_id=6, shop_id=2, count=50)
s6 = Stock(book_id=4, shop_id=3, count=10)
s7 = Stock(book_id=6, shop_id=3, count=10)
s8 = Stock(book_id=1, shop_id=2, count=10)
s9 = Stock(book_id=1, shop_id=3, count=10)

session.add_all([s1, s2, s3, s4, s5, s6, s7, s8, s9])
session.commit()

sl1 = Sale(price=50.05, date_sale="2018-10-25 09:45:24", stock_id=1, count=16)
sl2 = Sale(price=50.05, date_sale="2018-10-25 09:51:04", stock_id=3, count=10)
sl3 = Sale(price=10.50, date_sale="2018-10-25 09:52:22", stock_id=6, count=9)
sl4 = Sale(price=16.00, date_sale="2018-10-25 10:59:56", stock_id=5, count=5)
sl5 = Sale(price=16.00, date_sale="2018-10-25 10:59:56", stock_id=9, count=5)
sl6 = Sale(price=16.00, date_sale="2018-10-25 10:59:56", stock_id=4, count=1)

session.add_all([sl1, sl2, sl3, sl4, sl5, sl6])
session.commit()


publisher_name = input('Введите индификатор издателя:1 - OREILLY,2 - PEARSON,3 - MICROCOFT PRESS, 4 - NO STARCH PRESS ')

data = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
            .join(Publisher, Publisher.id == Book.publisher_id) \
            .join(Stock, Stock.book_id == Book.id) \
            .join(Shop, Shop.id == Stock.shop_id) \
            .join(Sale, Sale.stock_id == Stock.id) \
            .filter(Publisher.id == publisher_name).all()

for row in data:
    print(*row, sep=' | ')
