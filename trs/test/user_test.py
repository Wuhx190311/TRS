from trs.Role import *


def main():

    user2 = Customer('whx')
    admin = Admin()
    # user2.reserve_flight('1')
    # print(user2.request_all_info())
    # print(user2.get_reserved_info())
    # user2.cancel_flight('1')
    # print(user2.get_reserved_info())
    # user2.reserve_hotel(location='武汉')
    # print(user2.get_reserved_info())
    # user2.cancel_hotel('武汉')
    # print(user2.get_reserved_info())
    print(admin.request_all_info())
    print(admin.add_hotel(location='西安', price=300, rooms_num=100, avail_num=100))
    print(admin.request_all_info())


if __name__ == '__main__':
    main()
