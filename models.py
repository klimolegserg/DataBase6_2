from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=40), unique=True)

    def __str__(self):
        return f'{self.id} | {self.name}'


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(length=80), unique=True, nullable=False)
    publisher_id = Column(Integer, ForeignKey(Publisher.id), nullable=False)

    def __str__(self):
        return f'{self.id} | {self.title} | {self.publisher_id}'

    publisher = relationship(Publisher, backref='book')


class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=40), unique=True, nullable=False)

    def __str__(self):
        return f'{self.id} | {self.name}'


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    shop_id = Column(Integer, ForeignKey(Shop.id), nullable=False)
    count = Column(Integer, nullable=False)

    def __str__(self):
        return f'{self.id} | {self.book_id} | {self.shop_id} | {self.count}'

    book = relationship(Book, backref='stock')
    shop = relationship(Shop, backref='stock')


class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    price = Column(Numeric(5, 2), nullable=False)
    date_sale = Column(DateTime, nullable=False)
    stock_id = Column(Integer, ForeignKey(Stock.id), nullable=False)
    count = Column(Integer, nullable=False)

    def __str__(self):
        return f'{self.id} | {self.price} | {self.date_sale} | {self.stock_id} | {self.count}'

    stock = relationship(Stock, backref='sale')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
