from trs.DB_connector import DB_manager
from trs.DB_connector import Types
import trs.MyException.Resv_Exception as RE

"""
这个类基于DB_Connector实现了User拥有的方法
"""


class Resource_manager:
    def __init__(self):
        pass

    @staticmethod
    def get_userlist() -> list:
        cust_table = DB_manager.quire_customers()
        cust_list = []
        for customer in cust_table:
            # 不显示管理员账号
            if customer.id == '0':
                continue
            cust_info = {
                'id': customer.id,
                'name': customer.name,
            }
            cust_list.append(cust_info)
        return cust_list

    @staticmethod
    def get_bus_info(location=None):
        """
        返回全部bus的信息列表
        :param location 指定bus的主码
        :return: 一个字典的list,字典内容为{
                'location': bus.location,
                'price': bus.price,
                'bus_num': bus.bus_num,
                'avail_num': bus.avail_num,
                }
        """
        if location is not None:
            bus = DB_manager.quire_bus(primary_key=location)
            return bus
        info_list = DB_manager.quire_bus()
        buses_info = []
        for bus in info_list:
            bus_info = bus.to_dict()
            buses_info.append(bus_info)
        return buses_info

    @staticmethod
    def get_flight_info(flight_num=None):
        """
        返回全部航班表
        :param flight_num 航班号
        :return: 默认返回一个字典的list, 字典内容为 {
                'flight_num'
                'price'
                'seat_num'
                'avail_num'
                'from_city'
                'arrive_city'
            }
            当查询指定航班信息时，返回该航班的实例对象
        """

        if flight_num is not None:
            flight = DB_manager.quire_flight(primary_key=flight_num)
            return flight

        info_list = DB_manager.quire_flight()
        flights_info = []
        for flight in info_list:
            flight_info = flight.to_dict()
            flights_info.append(flight_info)
        return flights_info

    @staticmethod
    def get_hotel_info(location=None):
        """
        返回全部航班表
        :param location 指定酒店的主码
        :return: 一个字典的list, 字典内容为 {
                'location': hotel.location,
                'price': hotel.price,
                'rooms_num': hotel.hotel_num,
                'avail_num': hotel.avail_num,
            }
            当查询指定酒店信息时，返回该酒店的实例对象
        """

        if location is not None:
            hotel = DB_manager.quire_hotel(primary_key=location)
            return hotel

        info_list = DB_manager.quire_hotel()
        hotels_info = []
        for hotel in info_list:
            hotel_info = hotel.to_dict()
            hotels_info.append(hotel_info)
        return hotels_info

    @staticmethod
    def get_user_resv_info(username) -> list:
        """
        获得该用户的预约项
        :return 返回一个字典的数组，每个字典表示用户预约的项目
        """
        #
        # class demo:
        #
        #     def __init__(self, resvkey, cust_name, resv_type):
        #         self.resvkey = resvkey
        #         self.cust_name = cust_name
        #         self.resv_type = resv_type

        # Demo = [demo('1-1', 'whx', 1), demo('武汉-1', 'whx', 2)]
        # resv_list = Demo
        # 获得用户的预定表
        resv_list = DB_manager.quire_reservation(name=username)
        info_list = []
        for resv in resv_list:
            # 获得预约类型
            restype = Types(resv.get("resv_type"))
            # 获得预约的航班号、地址等信息

            item_id = str(resv.get("resvkey")).split('-')[1]
            # 查询相应表项，返回实例对象，若找不到返回None
            item = DB_manager.quire(restype, primary_key=item_id)
            if item is not None:
                info = item.to_dict()
                # 增加一个type: Types，标识字典类型
                info.update({"type": restype})
                info_list.append(info)
        return info_list

    @classmethod
    def get_user_travel_path(cls, username) -> str:
        info_list = cls.get_user_resv_info(username)
        if not info_list:
            return "None"

        info = info_list[0]
        info_type = info.get('type')

        type_dict = {
            Types.flight: lambda: info.get('arrive_city'),
            Types.bus: lambda: info.get('location'),
            Types.hotel: lambda: info.get('location')
        }

        return type_dict.get(info_type)()

    @staticmethod
    def reserve_item(username, primary_key, types: Types) -> str:
        """
        预定项目的通用接口
        :param username:
        :param primary_key:
        :param types: 预定的类型：Types.flight,Types.bus, Types.hotel
        :return: 返回预约信息
        """
        # 查询要预定的项目信息
        item = DB_manager.quire(types=types, primary_key=primary_key)
        if item is None:
            return "预定对象不存在！"
        # 没有剩余位置
        if item.avail_num <= 0:
            return "预定人数已满！"

        # 获得发出预定请求的用户信息
        cust = DB_manager.quire_customers(name=username)
        if cust is None:
            return "该用户不存在！"

        # 结构："type_id-item_primary_key-user_id"
        resvkey = str(types.value) + '-' + primary_key + '-' + str(cust.id)

        DB_manager.add_reservation(name=username, resvkey=resvkey, resv_type=types.value)

        # 更新item.avail_seat
        type_dict = {
            Types.flight: lambda: DB_manager.update_flight(primary_key=primary_key, types='resv'),
            Types.bus: lambda: DB_manager.update_bus(primary_key=primary_key, types='resv'),
            Types.hotel: lambda: DB_manager.update_hotel(primary_key=primary_key, types='resv'),
        }
        type_dict.get(types)()

        # 添加出错：如外键约束找不到用户
        try:
            DB_manager.db_change_commit()
            return "reserve successfully"
        except RE.ReservedItemException as e:
            return "您已经预定过该对象！"
        except Exception as e:
            return f"{e.args}"

    @staticmethod
    def cancel_item(username, primary_key, types: Types) -> str:
        """
        取消预定一个项目
        :param username: 发出取消请求的用户
        :param primary_key: 取消的项目的主键
        :param types: 取消项目的类型
        :return: 返回取消动作的msg:string
        """
        # 查询要取消的项目信息
        item = DB_manager.quire(types=types, primary_key=primary_key)
        if item is None:
            return "待取消对象不存在！"

        # 获得发出取消请求的用户信息
        cust = DB_manager.quire_customers(name=username)
        if cust is None:
            return "该用户不存在！"

        resvkey = str(types.value) + '-' + primary_key + '-' + str(cust.id)

        # 拿到用户resv信息，删除该项。如果用户未预定该项目，在commit时会捕获异常rollback
        resv = DB_manager.quire_reservation(name=username)
        DB_manager.delete_reservation(resvkey)

        # 更新item.avail
        type_dict = {
            Types.flight: lambda: DB_manager.update_flight(primary_key=primary_key, types='free'),
            Types.bus: lambda: DB_manager.update_bus(primary_key=primary_key, types='free'),
            Types.hotel: lambda: DB_manager.update_hotel(primary_key=primary_key, types='free'),
        }
        type_dict.get(types)()

        # 添加出错：如外键约束找不到用户
        try:
            DB_manager.db_change_commit()
            return "cancel successfully"
        except RE.ReservedItemException as e:
            return "您未预定过该对象！"
        except Exception as e:
            return f"{e.args}"

    @staticmethod
    def add_item(types: Types, **info):
        """
        管理员添加一项航班/巴士/酒店
        :param types:
        :param info:
            flight_info={
                flight_num=None,
                price=None,
                seat_num=None,
                avail_num=None,
                from_city=None,
                arrive_city=None
            }
            bus_info={location=None, price=None, bus_num=None, avail_num=None}
            hotel_info={location=None, price=None, rooms_num=None, avail_num=None}
        :return: msg:string
        """
        type_dict = {
            Types.flight: lambda: DB_manager.add_flight(**info),
            Types.bus: lambda: DB_manager.add_bus(**info),
            Types.hotel: lambda: DB_manager.add_hotel(**info),
        }
        msg = type_dict.get(types)()
        return msg

    @staticmethod
    def create_account(username: str) -> str:
        try:
            DB_manager.add_customer(name=username)
            DB_manager.db_change_commit()
            return "注册成功！"
        except RE.RegisteredUserException as e:
            return "该用户名已被注册！"
        except Exception as e:
            return e.args[0]

    @staticmethod
    def check_username(name: str) -> bool:
        """
        在数据库中查找是否存在指定用户
        :param name: 查找用户的姓名
        :return: 若数据库中有用户返回True,反之返回False
        """
        if DB_manager.quire_customers(name) is None:
            return False
        return True


if __name__ == '__main__':
    # Resource_manager.reserve_item('df', '2', Types.flight)

    pass
