from trs.Resource_manager import Resource_manager
from trs.DB_connector import Types
import trs.MyException.Resv_Exception as RE


class User:
    def __init__(self):
        self.resource_manager = Resource_manager

    def request_all_info(self) -> dict:
        """
        查询所有项目
        :return: dict:{"flights","buses","hotel"}
        """
        return {
            "flights": self.request_flight_info(),
            "buses": self.request_bus_info(),
            "hotels": self.request_hotel_info()
        }

    @staticmethod
    def request_flight_info() -> list:
        """
        :return: 一个字典的列表，每个字典为一班航班的信息
        """
        return Resource_manager.get_flight_info()

    @staticmethod
    def request_bus_info() -> list:
        """
        :return: 一个字典的列表，每个字典为一辆巴士的信息
        """
        return Resource_manager.get_bus_info()

    @staticmethod
    def request_hotel_info() -> list:
        """
        :return: 一个字典的列表，每个字典为一个酒店的信息
        """
        return Resource_manager.get_hotel_info()


class Visitor(User):
    def __init__(self):
        super().__init__()

    def login(self, username) -> User:
        """
        :return: 登录成功:Customer;
                 登录失败：Visitor
        """
        if username == 'admin':
            print("管理员登录成功！")
            return Admin()
        Has_registered = Resource_manager.check_username(name=username)
        # 如果是已注册用户，将对象实例切换为Customer
        if Has_registered:
            print('登录成功！')
            return Customer(username)
        else:
            print('未注册用户！')
            return self

    def signup(self, username: str):
        try:
            msg = Resource_manager.create_account(username)
            print(msg)
            if msg == "注册成功！":
                print("正在跳转....")
                return self.login(username)
            else:
                return self
        except RE.RegisteredUserException as e:
            print(e)
            return self
        # except Exception as e:
        #     print(e)


class Customer(User):
    """
    Customer的属性：
        :param self.name 姓名,
        :param: self.reserved_dict 记录已经预约了哪些项目
        :param: self.flights_reserved 一个列表，记录已预约所有的飞机信息
        :param: self.buses_reserved 一个列表，记录已预约的所有巴士信息（主键：地址）
        :param: self.hotels_reserved  一个列表，记录已预约的所有酒店信息（主键：地址）
    """

    def __init__(self, username):
        super().__init__()
        self.name = username

        # self.reserved_dict = {
        #     'flight': False,
        #     'bus': False,
        #     'hotel': False
        # }

        #
        """
        一个字典的列表，字典的key为：
        {"flight_id", "city_from", "city_arr"}
        """
        self.flights_reserved = []
        """
        一个记录buses的location的列表
        """
        self.buses_reserved = []
        """
        一个记录buses的location的列表
        """
        self.hotels_reserved = []

        # 初始化时将数据从数据库写入上面三个列表中
        self.__update_user_info()

    def __load_flight_resv(self, info: dict):
        """
        :param info:{'flight_num': flight.flight_num,
                     'price': flight.price,
                     'seat_num': flight.seat_num,
                     'avail_num': flight.avail_num,
                     'from_city': flight.from_city,
                     'arrive_city': flight.arrive_city}
        :return:
        """
        self.flights_reserved.append({
            "flight_id": info.get("flight_num"),
            "city_from": info.get("from_city"),
            "city_arr": info.get("arrive_city")
        })

    def __load_bus_resv(self, info: dict):
        """

        :param info: {  'location': bus.location,
                        'price': bus.price,
                        'bus_num': bus.bus_num,
                        'avail_num': bus.avail_num}
        :return:
        """

        self.buses_reserved.append(info.get('location'))

    def __load_hotel_resv(self, info: dict):
        """

        :param info: {  'location': hotel.location,
                        'price': hotel.price,
                        'hotel_num': hotel.hotel_num,
                        'avail_num': hotel.avail_num}
        :return:
        """
        self.hotels_reserved.append(info.get('location'))

    def __update_user_info(self):
        """
        用户初始化时从数据库中加载的预约信息
        """
        info_list = Resource_manager.get_user_resv_info(self.name)

        type_dict = {
            Types.flight: self.__load_flight_resv,
            Types.bus: self.__load_bus_resv,
            Types.hotel: self.__load_hotel_resv,
        }
        for info in info_list:
            type_dict.get(info.get('type'))(info)


    def logout(self) -> Visitor:
        del self
        return Visitor()

    def get_reserved_info(self) -> dict:
        """
        用户获得自己的预定信息
        :return: dict={
            'flight': self.flight_reserved,
            'bus': self.bus_reserved_location,
            'hotel': self.hotel_reserved_location
        }
        """
        return {
            'flight': self.flights_reserved,
            'bus': self.buses_reserved,
            'hotel': self.hotels_reserved
        }

    def cancel_flight(self, flight_num: str):
        # 未预定过
        if flight_num not in [f.get('flight_id') for f in self.flights_reserved]:
            print(f"您未预定过id为{flight_num}的航班！")
            return

        msg = Resource_manager.cancel_item(self.name, primary_key=flight_num, types=Types.flight)
        if "cancel successfully" != msg:
            print(msg)
            return

        flight_to_be_canceled = None
        for f in self.flights_reserved:
            if f.get('flight_id') == flight_num:
                flight_to_be_canceled = f
        self.flights_reserved.remove(flight_to_be_canceled)
        print(
            f"成功取消航班：{flight_num}")

    def cancel_bus(self, location: str):
        # 未预定过
        if location not in self.buses_reserved:
            print(f"您未预定过{location}的巴士")
            return

        msg = Resource_manager.cancel_item(self.name, primary_key=location, types=Types.bus)
        if "cancel successfully" != msg:
            print(msg)
            return

        self.buses_reserved.remove(location)
        print(
            f"成功取消巴士，地址：{location}")

    def cancel_hotel(self, location: str):
        # 未预定过
        if location not in self.hotels_reserved:
            print(f"您未预定过{location}的酒店")
            return

        msg = Resource_manager.cancel_item(self.name, primary_key=location, types=Types.hotel)
        if "cancel successfully" != msg:
            print(msg)
            return

        self.hotels_reserved.remove(location)
        print(
            f"成功取消酒店，地址：{location}")

    def reserve_flight(self, flight_num: str):

        # 已预定过
        if flight_num in [f.get('flight_id') for f in self.flights_reserved]:
            print(f"您已预定过id为{flight_num}的航班！")
            return

        msg = Resource_manager.reserve_item(self.name, primary_key=flight_num, types=Types.flight)

        # 预定失败
        if "reserve successfully" != msg:
            print(msg)
            return

        # 获取该次航班信息，并在用户属性中保存
        flight = Resource_manager.get_flight_info(flight_num=flight_num)
        if flight is None:
            # 程序永不不会执行此条语句
            return

        self.flights_reserved.append({
            'flight_id': flight.flight_num,
            'city_from': flight.from_city,
            'city_arr': flight.arrive_city
        })

        # self.reserved_dict['flight'] = True
        print(
            f"预定成功：航班号:{flight.flight_num}, 出发地:{flight.from_city}, 目的地{flight.arrive_city}")

    def reserve_bus(self, location):
        if location in self.buses_reserved:
            print(f"您已预定过{location}的巴士")
            return

        msg = Resource_manager.reserve_item(self.name, primary_key=location, types=Types.bus)

        # 预定失败
        if "reserve successfully" != msg:
            print(msg)
            return

        # 将预定信息保存在属性中
        self.buses_reserved.append(location)
        print(f"预定成功：地址:{location}")

    def reserve_hotel(self, location):
        if location in self.hotels_reserved:
            print(f"您已预定过{location}的酒店")
            return

        msg = Resource_manager.reserve_item(self.name, primary_key=location, types=Types.hotel)

        # 预定失败
        if "reserve successfully" != msg:
            print(msg)
            return

        self.hotels_reserved.append(location)
        print(f"预定成功：地址:{location}")

    def get_travel_path(self):
        return self.hotel_reserved_location

    def check_full_path(self):
        pass


class Admin(Customer):
    def __init__(self):
        super().__init__(username='admin')
        pass

    @staticmethod
    def add_flight(flight_num=None, price=None, seat_num=None, avail_num=None, from_city=None, arrive_city=None):
        msg = Resource_manager.add_item(types=Types.flight, flight_num=flight_num, price=price, seat_num=seat_num,
                                        avail_num=avail_num, from_city=from_city, arrive_city=arrive_city)
        return msg

    @staticmethod
    def add_bus(location=None, price=None, bus_num=None, avail_num=None):
        msg = Resource_manager.add_item(types=Types.bus, location=location, price=price, bus_num=bus_num,
                                        avail_num=avail_num)
        return msg

    @staticmethod
    def add_hotel(location=None, price=None, rooms_num=None, avail_num=None):
        msg = Resource_manager.add_item(types=Types.hotel, location=location, price=price, rooms_num=rooms_num,
                                        avail_num=avail_num)
        return msg

    @staticmethod
    def get_user_list():
        return Resource_manager.get_userlist()
