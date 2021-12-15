from enum import Enum

import sqlalchemy
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
import trs.MyException.Resv_Exception as RE

Base = declarative_base()


class Types(Enum):
    flight = 1
    bus = 2
    hotel = 3


class Item:
    def to_dict(self) -> dict:
        pass


class Flight(Base, Item):
    __tablename__ = 'Flight'
    flight_num = Column(String(20), primary_key=True)
    price = Column(Integer)
    seat_num = Column(Integer)
    avail_num = Column(Integer)
    from_city = Column(String(20))
    arrive_city = Column(String(20))

    def to_dict(self) -> dict:
        return {
            'flight_num': self.flight_num,
            'price': self.price,
            'seat_num': self.seat_num,
            'avail_num': self.avail_num,
            'from_city': self.from_city,
            'arrive_city': self.arrive_city
        }


class Bus(Base, Item):
    __tablename__ = 'Bus'
    location = Column(String(20), primary_key=True)
    price = Column(Integer)
    bus_num = Column(Integer)
    avail_num = Column(Integer)

    def to_dict(self):
        return {
            'location': self.location,
            'price': self.price,
            'bus_num': self.bus_num,
            'avail_num': self.avail_num,
        }


class Hotel(Base, Item):
    __tablename__ = 'Hotel'
    location = Column(String(20), primary_key=True)
    price = Column(Integer)
    rooms_num = Column(Integer)
    avail_num = Column(Integer)

    def to_dict(self) -> dict:
        return {
            'location': self.location,
            'price': self.price,
            'rooms_num': self.rooms_num,
            'avail_num': self.avail_num,
        }


class Reservation(Base):
    __tablename__ = 'Reservation'

    # resvkey 结构为 item_id-user_id, 如 “1-1” 为id为1的用户预定了一号航班（假设）
    resvkey = Column(String(20), primary_key=True)
    cust_name = Column(String(20), ForeignKey("Customers.name"))
    resv_type = Column(Integer)

    # 与Customer关联查询
    customer = relationship("Customers", backref="resv", cascade='all, delete')  # delete on cascade


class Customers(Base):
    __tablename__ = 'Customers'
    name = Column(String(20), primary_key=True)
    id = Column(Integer)


class DB_manager:
    engine = create_engine("mysql+pymysql://root:123456@localhost/trs?charset=utf8", echo=False)    # TODO: TAG
    # raised as a result of Query-invoked autoflush;
    # consider using a session.no_autoflush block if this flush is occurring prematurely
    # 这里需要关闭数据库自动刷新，否则会出现新、旧实例冲突的问题
    Session_cls = sessionmaker(bind=engine, autoflush=False)
    Session = Session_cls()

    @classmethod
    def db_change_commit(cls):
        try:
            cls.Session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            cls.Session.rollback()
            if "Duplicate entry" in e.args[0]:
                # 重复预定
                if "reservation" in e.args[0]:
                    raise RE.ReservedItemException

                # 重复用户
                elif "customers" in e.args[0]:
                    raise RE.RegisteredUserException
                else:
                    raise Exception
        except Exception:
            cls.Session.rollback()
            raise

    @classmethod
    def db_rollback(cls):
        cls.Session.rollback()

    @classmethod
    def quire(cls, types: Types, primary_key=None) -> Item:
        """
        :param types: 查询种类, 类型为 DB_connector.Types
        :param primary_key:
        :return:    1.不指定primary_key时：    返回一个所有item信息的list，
                    2.指定primary_key时：    返回该item的一个数据封装类对象，若找不到则返回None
        """
        type_dict = {
            Types.flight: cls.quire_flight,
            Types.bus: cls.quire_bus,
            Types.hotel: cls.quire_hotel
        }

        return type_dict.get(types)(primary_key=primary_key)

    @classmethod
    def quire_flight(cls, primary_key=None):
        """
        :param primary_key:
        :return:    1.不指定primary_key时：    返回一个所有flight信息的list，
                    2.指定primary_key时：    返回该flight的一个数据封装类，若找不到则返回None
        """
        if primary_key is None:
            flight_table = cls.Session.query(Flight).all()
        else:
            flight_table = cls.Session.query(Flight).filter(Flight.flight_num == f'{primary_key}').first()
        return flight_table

    @classmethod
    def quire_bus(cls, primary_key=None) -> list:
        """获取巴士信息"""
        if primary_key is None:
            bus_table = cls.Session.query(Bus).all()
        else:
            bus_table = cls.Session.query(Bus).filter(Bus.location == f'{primary_key}').first()
        return bus_table

    @classmethod
    def quire_hotel(cls, primary_key=None):
        """获取酒店信息"""
        if primary_key is None:
            hotel_table = cls.Session.query(Hotel).all()
        else:
            hotel_table = cls.Session.query(Hotel).filter(Hotel.location == f'{primary_key}').first()
        return hotel_table

    @classmethod
    def quire_customers(cls, name=''):
        """
        :param name: 默认为空，此时查询所有用户的名单
        :return:    1.不指定用户时：    返回一个所有用户的名单list，
                        [{'id': 2, 'name': 'a'}, {'id': 0, 'name': 'admin'}],
                    2.指定查找用户时：    返回该用户的一个数据封装类，若找不到用户则返None
        """
        if name == '':
            cust = cls.Session.query(Customers).all()
        else:
            cust = cls.Session.query(Customers).filter(Customers.name == f'{name}').first()
        return cust

    @classmethod
    def quire_reservation(cls, name='') -> list:
        """

        :param name: 预定用户的名字
        :return: 一个字典的数组，字典内容为：
            resv_info = {
                'resvkey': reservation.resvkey,
                'cust_name': reservation.cust_name,
                'resv_type': reservation.resv_type
            }
        """
        if name == '':
            resv_table = cls.Session.query(Reservation).all()
        else:
            resv_table = cls.Session.query(Reservation).filter(Reservation.cust_name == f'{name}').all()
        resv_list = []
        for reservation in resv_table:
            resv_info = {
                'resvkey': reservation.resvkey,
                'cust_name': reservation.cust_name,
                'resv_type': reservation.resv_type
            }
            resv_list.append(resv_info)
        return resv_list

    @classmethod
    def update_flight(cls, primary_key: str, types: str):
        """
        :param primary_key: 主码，唯一确定需要更新的行
        :param types: 更新的方式，“resv”为预定，avail-1;“free”为取消预定，avail+1
        """
        flight = cls.Session.query(Flight).filter(Flight.flight_num == f'{primary_key}').first()
        type_dict = {
            "resv": lambda: flight.avail_num - 1,
            "free": lambda: flight.avail_num + 1
        }
        flight.avail_num = type_dict.get(types)()

    @classmethod
    def update_bus(cls, primary_key: str, types: str):
        """
        :param primary_key: 主码，唯一确定需要更新的行
        :param types: 更新的方式，“resv”为预定，avail-1;“free”为取消预定，avail+1
        """
        bus = cls.Session.query(Bus).filter(Bus.location == f'{primary_key}').first()
        type_dict = {
            "resv": lambda: bus.avail_num - 1,
            "free": lambda: bus.avail_num + 1
        }
        bus.avail_num = type_dict.get(types)()
        # cls.Session.commit()

    @classmethod
    def update_hotel(cls, primary_key, types: str):
        """
        :param primary_key: 主码，唯一确定需要更新的行
        :param types: 更新的方式，“resv”为预定，avail-1;“free”为取消预定，avail+1
        """
        hotel = cls.Session.query(Hotel).filter(Hotel.location == f'{primary_key}').first()
        type_dict = {
            "resv": lambda: hotel.avail_num - 1,
            "free": lambda: hotel.avail_num + 1
        }
        hotel.avail_num = type_dict.get(types)()
        # cls.Session.commit()

    @classmethod
    def add_flight(cls, flight_num=None, price=None, seat_num=None, avail_num=None, from_city=None, arrive_city=None) -> str:
        flight = Flight(flight_num=flight_num,
                        price=price,
                        seat_num=seat_num,
                        avail_num=avail_num,
                        from_city=from_city,
                        arrive_city=arrive_city)
        try:
            cls.Session.add(flight)
            cls.Session.commit()
            return f'成功增加航班,id={flight_num}'
        except sqlalchemy.exc.IntegrityError:
            cls.Session.rollback()
            return '已存在该航班'

    @classmethod
    def add_bus(cls, location=None, price=None, bus_num=None, avail_num=None):
        bus = Bus(location=location, price=price, bus_num=bus_num, avail_num=avail_num)
        try:
            cls.Session.add(bus)
            cls.Session.commit()
            return f'成功增加巴士，location={location}'
        except sqlalchemy.exc.IntegrityError:
            cls.Session.rollback()
            return '已存在这班巴士'

    @classmethod
    def add_hotel(cls, location=None, price=None, rooms_num=None, avail_num=None):
        hotel = Hotel(location=location, price=price, rooms_num=rooms_num, avail_num=avail_num)
        try:
            cls.Session.add(hotel)
            cls.Session.commit()
            return f'成功增加酒店，location={location}'
        except sqlalchemy.exc.IntegrityError:
            cls.Session.rollback()
            return '已存在该酒店'

    @classmethod
    def add_customer(cls, name):
        last_id = cls.Session.query(Customers.id).order_by(Customers.id.desc()).first()[0]
        cust = Customers(name=name, id=last_id + 1)
        try:
            cls.Session.add(cust)
        except sqlalchemy.exc.IntegrityError as e:
            raise RE.RegisteredUserException

    @classmethod
    def add_reservation(cls, name, resvkey: str, resv_type):
        resv = Reservation(resvkey=resvkey, cust_name=name, resv_type=resv_type)
        cls.Session.add(resv)

    @classmethod
    def delete_flight(cls, flight_num):
        cls.Session.query(Flight).filter(Flight.flight_num == flight_num).delete()
        cls.Session.commit()

    @classmethod
    def delete_bus(cls, location):
        cls.Session.query(Bus).filter(Bus.location == location).delete()
        cls.Session.commit()

    @classmethod
    def delete_hotel(cls, location):
        cls.Session.query(Hotel).filter(Hotel.location == location).delete()
        cls.Session.commit()

    @classmethod
    def delete_customer(cls, name):
        # 外键约束，当删除用户时，会同步删除所有reservation信息
        resv_list = DB_manager.quire_reservation(name=username)
        for resv in resv_list:
            # 获得预约类型
            restype = Types(resv.resv_type)
            # 获得预约的航班号、地址等信息
            item_id = str(resv.resvkey).split('-')[0]
            # 查询相应表项，表中元素唯一
            type_dict = {
                Types.flight: lambda: cls.Session.query(Flight).filter(Flight.flight_num == item_id),
                Types.bus: lambda: cls.Session.query(Bus).filter(Bus.location == item_id),
                Types.hotel: lambda: cls.Session.query(Hotel).filter(Hotel.location == item_id)
            }
            item = type_dict.get(restype)()
            item.avail_num += 1
        cls.Session.query(Customers).filter(Customers.name == name).delete()
        # cls.Session.commit()

    @classmethod
    def delete_reservation(cls, primary_key):
        # 同时要将所有预定的信息还原
        cls.Session.query(Reservation).filter(Reservation.resvkey == primary_key).delete()
        # cls.Session.commit()


if __name__ == '__main__':
    # DB_manager.update_flight('2', types='free')
    # DB_manager.add_customer('df')
    # DB_manager.delete_reservation('df',)
    # DB_manager.delete_customer('df')
    # DB_manager.add_reservation('df', '1-2', 1)
    # DB_manager.add_flight(flight_num='1', price=1000, seat_num=150, avail_num=150, from_city='西安', arrive_city='武汉')
    # print(Types(1))
    # print(DB_manager.quire_customers(username='sss'))
    # print(DB_manager.get_user_resv_info('whx'))
    # print(DB_manager.quire(Types.flight))
    # s = '1234-1234'
    # print(s.split('-'))
    # print(DB_manager.get_user_travel_path('whx'))
    # DB_manager.resv_flight('1')
    # print(DB_manager.quire_flight())
    # for _ in range(80):
    #     DB_manager.update_hotel('武汉', 'free')
    #     DB_manager.Session.commit()
    pass
