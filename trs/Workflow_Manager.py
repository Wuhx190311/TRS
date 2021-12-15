from enum import Enum
from trs.Role import *
from functools import cmp_to_key


class Workflow_manager:

    def __init__(self):
        self.user = Visitor()

    def user_login(self, username):
        if isinstance(self.user, Visitor):
            self.user = self.user.login(username)

    def user_signup(self, username):
        self.user = self.user.signup(username)

    def user_request_info(self):
        """查看航班、旅馆、巴士等信息"""
        info_dict = self.user.request_all_info()
        flight_list = info_dict.get('flights')
        if not flight_list:
            print('未安排航班')
        else:
            print('航班信息:')
            index = 0
            for item in flight_list:
                index += 1
                print(f'{index}. 航班号:', item.get('flight_num'), '价格:', item.get('price'), '剩余座位:',
                      item.get('avail_num'),
                      '  行程：', item.get('from_city'), '====>', item.get('arrive_city'))

        bus_list = info_dict.get('buses')
        if not bus_list:
            print('未安排大巴')
        else:
            print('大巴信息:')
            index = 0
            for item in bus_list:
                index += 1
                print(f'{index}. 地址:', item.get('location'), '价格:', item.get('price'), '剩余座位:', item.get('avail_num'))

        hotel_list = info_dict.get('hotels')
        if not hotel_list:
            print('未安排酒店')
        else:
            print('酒店信息:')
            index = 0
            for item in hotel_list:
                index += 1
                print(f'{index}. 地址:', item.get('location'), '价格:', item.get('price'), '剩余房间:', item.get('avail_num'))

    def user_logout(self):
        self.user = self.user.logout()

    def user_require_my_reservation(self):
        if isinstance(self.user, Customer):
            info_dict = self.user.get_reserved_info()
            flight_list = info_dict.get('flight')
            if not flight_list:
                print('已预定的航班：尚未预定')
            else:
                print('已预定的航班:')
                index = 0
                for item in flight_list:
                    index += 1
                    print(f'{index}. 航班号:', item.get('flight_id'), '  行程：', item.get('city_from'), '====>',
                          item.get('city_arr'))

            bus_list = info_dict.get('bus')
            if not bus_list:
                print('已预定的大巴:尚未预定')
            else:
                print('已预定的大巴：', bus_list)

            hotel_list = info_dict.get('hotel')
            if not hotel_list:
                print('已预定的酒店：尚未预定')
            else:
                print('已预定的酒店：', hotel_list)
        else:
            print('用户未登录！')

    def user_reserve_flight(self, flight_num):
        if isinstance(self.user, Visitor):
            print('用户未登录')
            return
        self.user.reserve_flight(flight_num)

    def user_reserve_bus(self, location):
        if isinstance(self.user, Visitor):
            print('用户未登录')
            return
        self.user.reserve_bus(location)

    def user_reserve_hotel(self, location):
        if isinstance(self.user, Visitor):
            print('用户未登录')
            return
        self.user.reserve_hotel(location)

    def user_cancel_flight(self, flight_num):
        if isinstance(self.user, Visitor):
            print('用户未登录')
            return
        self.user.cancel_flight(flight_num)

    def user_cancel_bus(self, location):
        if isinstance(self.user, Visitor):
            print('用户未登录')
            return
        self.user.cancel_bus(location)

    def user_cancel_hotel(self, location):
        if isinstance(self.user, Visitor):
            print('用户未登录')
            return
        self.user.cancel_hotel(location)

    def user_require_travel_path(self):
        if isinstance(self.user, Visitor):
            print('用户未登录')
            return
        print(self.user.get_travel_path)

    def user_detect_complete_path(self):
        """查看自己预定的路径是否完整：是否飞机、酒店、巴士均已经预定，且都在一个城市"""
        pass

    def admin_add_flight(self, flight_num=None, price=None, seat_num=None, avail_num=None, from_city=None,
                         arrive_city=None):
        if isinstance(self.user, Admin):
            print(self.user.add_flight(flight_num=flight_num, price=price, seat_num=seat_num,
                                       avail_num=avail_num, from_city=from_city, arrive_city=arrive_city))
        else:
            print('该用户无操作权限')

    def admin_add_bus(self, location=None, price=None, bus_num=None, avail_num=None):
        if isinstance(self.user, Admin):
            print(self.user.add_bus(location=location, price=price, bus_num=bus_num, avail_num=avail_num))
        else:
            print('该用户无操作权限')

    def admin_add_hotel(self, location=None, price=None, rooms_num=None, avail_num=None):
        if isinstance(self.user, Admin):
            print(self.user.add_hotel(location=location, price=price, rooms_num=rooms_num,
                                      avail_num=avail_num))
        else:
            print('该用户无操作权限')

    def admin_get_userlist(self):
        if isinstance(self.user, Admin):
            users_list = self.user.get_user_list()
            users_list.sort(key=cmp_to_key(lambda x, y: int(x.get('id')) - int(y.get('id'))))
            for user in users_list:
                user_id = user.get('id')
                name = user.get('name')
                print(f'id:{user_id} name:{name}')

    def admin_get_info(self):
        if isinstance(self.user, Admin):
            info_dict = self.user.request_all_info()
            flight_list = info_dict.get('flights')
            print()
            if not flight_list:
                print('未安排航班')
            else:
                print('航班信息:')
                index = 0
                for item in flight_list:
                    index += 1
                    print(f'{index}. 航班号:', item.get('flight_num'), '价格:', item.get('price'), '总座位数',
                          item.get('seat_num'), '剩余座位', item.get('avail_num'),
                          '  行程：', item.get('from_city'), '====>', item.get('arrive_city'))

            bus_list = info_dict.get('buses')
            print()
            if not bus_list:
                print('未安排大巴')
            else:
                print('大巴信息:')
                index = 0
                for item in bus_list:
                    index += 1
                    print(f'{index}. 地址:', item.get('location'), '价格:', item.get('price'),
                          '总座位数:', item.get('bus_num'), '剩余座位数', item.get('avail_num'))

            hotel_list = info_dict.get('hotels')
            print()
            if not hotel_list:
                print('未安排酒店')
            else:
                print('酒店信息:')
                index = 0
                for item in hotel_list:
                    index += 1
                    print(f'{index}. 地址:', item.get('location'), '价格:', item.get('price'),
                          '总房间数:', item.get('rooms_num'), '剩余房间数:', item.get('avail_num'))


if __name__ == '__main__':
    pass
