from trs.Workflow_Manager import Workflow_manager
from trs.DB_connector import Types
from trs.Role import *

type_dict = {
    'flight': Types.flight,
    'bus': Types.bus,
    'hotel': Types.hotel
}


def reserve(wf: Workflow_manager):
    flag = True
    while flag:
        print('1.flight 2.bus 3.hotel')
        input_types = input('请输入要预定的类型：')
        types = type_dict.get(input_types)
        if types is None:
            print()
            print('类型输入错误，请重新输入！')
            print()
            continue
        if types == Types.flight:
            flight_list = wf.user.request_flight_info()
            if not flight_list:
                print('未安排航班')
            else:
                print()
                print('航班信息:')
                index = 0
                for item in flight_list:
                    index += 1
                    print(f'{index}. 航班号:', item.get('flight_num'), '价格', item.get('price'), '剩余座位',
                          item.get('avail_num'),
                          '  行程：', item.get('from_city'), '====>', item.get('arrive_city'))

            wf.user_reserve_flight(input('请输入要预定的航班号：'))
        if types == Types.bus:
            bus_list = wf.user.request_bus_info()
            if not bus_list:
                print('未安排大巴')
            else:
                print()
                print('大巴信息:')
                index = 0
                for item in bus_list:
                    index += 1
                    print(f'{index}. 地址:', item.get('location'), '价格', item.get('price'), '剩余座位', item.get('avail_num'))

            wf.user_reserve_bus(input('请输入预定巴士的地址:'))
        if types == Types.hotel:
            hotel_list = wf.user.request_hotel_info()
            if not hotel_list:
                print('未安排酒店')
            else:
                print()
                print('酒店信息:')
                index = 0
                for item in hotel_list:
                    index += 1
                    print(f'{index}. 地址:', item.get('location'), '价格', item.get('price'), '剩余座位', item.get('avail_num'))

            wf.user_reserve_hotel(input('请输入预定酒店的地址:'))
        print('是否返回上一级？ Y：是， N：否')
        cmd = input()
        if cmd == 'Y' or cmd == 'y':
            flag = False


def cancel(wf: Workflow_manager):
    print('已预定的项目：')
    wf.user_require_my_reservation()
    flag = True
    while flag:
        print()
        print('1.flight 2.bus 3.hotel')
        input_types = input('请输入要取消预定的类型：')
        types = type_dict.get(input_types)
        if types is None:
            print()
            print('类型输入错误，请重新输入！')
            print()
            continue
        if types == Types.flight:
            wf.user_cancel_flight(input('请输入要取消预定的航班号：'))
        if types == Types.bus:
            wf.user_cancel_bus(input('请输入要取消预定的巴士地址：'))
        if types == Types.hotel:
            wf.user_cancel_hotel(input('请输入要取消预定的酒店地址：'))
        print('是否返回上一级？ Y：是， N：否')
        cmd = input()
        if cmd == 'Y' or cmd == 'y':
            flag = False


def add(wf: Workflow_manager):
    print('已存在的项目：')
    wf.user_request_info()
    flag = True
    while flag:
        print()
        print('1.flight 2.bus 3.hotel')
        input_types = input('请输入要新增的类型：')
        types = type_dict.get(input_types)
        if types is None:
            print()
            print('类型输入错误，请重新输入！')
            print()
            continue
        if types == Types.flight:
            msg_correct = False
            while not msg_correct:
                print()
                flight_num = input('请输入新增的航班号：')
                price = input('请输入航班票价：')
                city_from = input('请输入始发城市：')
                city_arr = input('请输入目的城市：')
                seat_num = input('请输入座位数：')
                avail_num = seat_num
                print()
                print('确认新增航班信息：')
                print(f'航班号：{flight_num}, 票价：{price}, 座位数：{seat_num}, 始发地：{city_from}, 目的地：{city_arr}')
                print('信息是否正确？ Y：是， N：否')
                cmd = input()
                if cmd == 'Y' or cmd == 'y':
                    msg_correct = True
                    wf.admin_add_flight(flight_num, price, seat_num, avail_num, city_from, city_arr)
                else:
                    print('重新输入信息：')
                    continue
        if types == Types.bus:
            msg_correct = False
            while not msg_correct:
                print()
                location = input('请输入新增巴士的地址：')
                price = input('请输入巴士票价：')
                bus_num = input('请输入座位数：')
                avail_num = bus_num
                print()
                print('确认新增巴士信息：')
                print(f'地址：{location}, 票价：{price}, 座位数：{bus_num}')
                print('信息是否正确？ Y：是， N：否')
                cmd = input()
                if cmd == 'Y' or cmd == 'y':
                    msg_correct = True
                    wf.admin_add_bus(location, price, bus_num, avail_num)
                else:
                    print('重新输入信息：')
                    continue
        if types == Types.hotel:
            msg_correct = False
            while not msg_correct:
                print()
                location = input('请输入新增酒店的地址：')
                price = input('请输入酒店房间价格：')
                rooms_num = input('请输入酒店房间数：')
                avail_num = rooms_num
                print()
                print('确认新增酒店信息：')
                print(f'地址：{location}, 房间价格：{price}, 房间数：{rooms_num}')
                print('信息是否正确？ Y：是， N：否')
                cmd = input()
                if cmd == 'Y' or cmd == 'y':
                    msg_correct = True
                    wf.admin_add_hotel(location, price, rooms_num, avail_num)
                else:
                    print('重新输入信息：')
                    continue
        print('是否返回上一级？ Y：是， N：否')
        cmd = input()
        if cmd == 'Y' or cmd == 'y':
            flag = False


def main():
    workflow1 = Workflow_manager()

    command_dict = {
        # 权限等级：Visitor

        ## 登录操作
        'sign up': lambda: workflow1.user_signup(input('新建用户名：')),
        'login': lambda: workflow1.user_login(input('请输入用户名：')),

        ## 查询项目操作
        'quire': lambda: workflow1.admin_get_info() if isinstance(workflow1.user, Admin) else workflow1.user_request_info(),

        # 权限等级: Customer

        ## 登出操作
        'logout': lambda: workflow1.user_logout(),

        ## 预定/取消预定操作
        'reserve': reserve,
        'cancel': cancel,

        ## 查看自己信息
        'my resv': lambda: workflow1.user_require_my_reservation(),

        # 权限等级：Admin
        # 增加项目操作
        'add': add,
        'list users': lambda: workflow1.admin_get_userlist()

    }
    while True:
        print('1.sign up 2.login 3.quire 4.exit')
        cmd = input('Visitor>')
        if cmd == 'exit':
            print('退出...')
            return 0
        try:
            func = command_dict.get(cmd)
            func()
        except TypeError:
            print('指令输入错误，请重新输入指令！')
            print()
            continue
        while isinstance(workflow1.user, Admin):
            print('1.quire 2.add 3.list users 4.logout 5.exit')
            cmd = input('Admin#')
            if cmd == 'exit':
                print('退出...')
                return 0
            func = command_dict.get(cmd)
            if func is None:
                print('指令输入错误，请重新输入指令！')
                print()
                continue
            if cmd in ['quire', 'list users', 'logout']:
                func()
            elif cmd == 'add':
                func(workflow1)
            else:
                return -1
        while isinstance(workflow1.user, Customer):
            print('1.quire 2.reserve 3.cancel 4.my resv 5.logout 6.exit')
            cmd = input(f'{workflow1.user.name}$')
            if cmd == 'exit':
                print('退出...')
                return 0
            func = command_dict.get(cmd)
            if func is None:
                print('指令输入错误，请重新输入指令！')
                print()
                continue
            if cmd in ['quire', 'my resv', 'logout']:
                func()
            elif cmd in ['reserve', 'cancel']:
                func(workflow1)
            else:
                # 程序永远不会运行至此处
                return -1


if __name__ == '__main__':
    main()
