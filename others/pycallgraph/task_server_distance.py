import socket
from threading import Thread
import json
import time
import csv
from geopy.distance import geodesic
import math


ADDRESS = ('0.0.0.0', 8712)  # 绑定地址
g_socket_server = None  # 负责监听的socket
g_conn_pool = {}  # 连接池

LAT = 'lat'
LON = 'lon'
ALT = 'alt'
CMD = 'cmd'
TIME = 'time'
ground_lat = 30.28708
ground_lon = 120.12802999999997
ground_alt = 40.23141

UAV_FLY = 'FLY'
TIME_TEST = 'delay_time'
SEND_GROUND_LOCATION = 'send_g_l'
SET_G_LOCATION = 'set_g_l'
SET_G_L = 'set'
CAL_DIST_2UAV = 'cal_uavs'
CAL_DIST_G_U = 'dist_uav'
QUERY_BATTERY = 'battery'
CONNECT = 'connect'
SEND_DATA = 'send_data'
UAV_INFO = 'uav_info'

# Drone Fix CMD
CHANGE_PARAM_BAD = 'bad'
CHANGE_PARAM_GOOD = 'good'


COUNT_UAVs = 0
uav_location = []
delay_list = []


def init():
    """
    初始化服务端
    """
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    g_socket_server.bind(ADDRESS)
    g_socket_server.listen(10)  # 最大等待数（有很多人理解为最大连接数，其实是错误的）
    print("server start，wait for client connecting...")


def accept_client():

    """
    接收新连接
    """
    while True:
        client, info = g_socket_server.accept()  # 阻塞，等待客户端连接
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=message_handle, args=(client, info))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()


def message_handle(client, info):
    """
    消息处理
    """
    global ground_lat, ground_lon, ground_alt

    client.sendall("connect server successfully!".encode(encoding='utf8'))
    while True:
        try:
            bytes = client.recv(2048)
            rec_time = time.time()
            msg = json.loads(bytes.decode(encoding='utf8'))
            cmd = msg[CMD]
            client_name = msg['client_name']

            if cmd == CONNECT:
                g_conn_pool[client_name] = client
                print('on client connect: ' + client_name, info)
            elif cmd == SEND_DATA:
                print(client_name + ': ' + msg[UAV_INFO])
            elif cmd == SET_G_LOCATION:
                ground_lat, ground_lon, ground_alt = msg[LAT], msg[LON], msg[ALT]
                print('地面站设置了lat：%lf, lon:%lf, alt: %lf' % (ground_lat, ground_lon, ground_alt))
            elif cmd == CAL_DIST_2UAV:
                cal_dist_uavs(msg[LAT], msg[LON], msg[ALT], client_name)
            elif cmd == CAL_DIST_G_U:
                l_dist = geodesic((msg[LAT], msg[LON]), (ground_lat, ground_lon)).meters
                h_dist = msg[ALT] - ground_alt
                dist = math.sqrt(l_dist * l_dist + h_dist * h_dist)
                print('distance between %s to ground: %lf m' % (client_name, dist))
            elif cmd == TIME_TEST:
                delay_time = (rec_time - msg[TIME]) * 1000 / 2
                i = msg['index'] + 1
                delay_list.append([i, delay_time])
                if i == msg['total']:
                    with open(msg['file'] + '.csv', 'a', encoding='utf-8', newline='') as file_obj:
                        writer = csv.writer(file_obj)
                        writer.writerows(delay_list)
                    delay_list = []
                    print('finish write %s' % msg['file'])

        except Exception as e:
            print(e)
            remove_client(client_name)
            break


def cal_dist_uavs(uav1_lat, uav1_lon, uav1_alt, client_name):
    global uav_location
    global COUNT_UAVs
    print('%s: lat : %lf ,lon: %lf, alt:%lf' % (client_name, uav1_lat, uav1_lon, uav1_alt))
    uav_location.append(uav1_lat)
    uav_location.append(uav1_lon)
    uav_location.append(uav1_alt)
    COUNT_UAVs += 1

    if COUNT_UAVs == 2:
        COUNT_UAVs = 0
        l_dist = geodesic((uav_location[0], uav_location[1]), (uav_location[3], uav_location[4])).meters
        h_dist = uav_location[2] - uav_location[5]
        dist_two_uav = math.sqrt(l_dist * l_dist + h_dist * h_dist)
        print('之间的距离为：%lf m' % dist_two_uav)
        uav_location = []


def remove_client(client_name):
    client = g_conn_pool[client_name]
    if client is not None:
        client.close()
        g_conn_pool.pop(client_name)
        print("client offline: " + client_name)


def send_data(op):

    if op == 'all':
        all_uavs_fly()
    # elif op == 'bdc':
    #     task_c()
    elif op == 'bd0':
         taskf()
    elif op == 'multi':
        multi_uav_fly()
    elif op == TIME_TEST:
        for client_name, uav in g_conn_pool.items():
            time_test(client_name, uav)
    elif op == SEND_GROUND_LOCATION:
        send_ground_location()
    elif op in (SET_G_LOCATION, CAL_DIST_G_U):
        set_ground_location(op)
    elif op == SET_G_L:
        set_g_l()
    elif op == CAL_DIST_2UAV:
        cal_2_uavs()

    elif op in (QUERY_BATTERY, CHANGE_PARAM_GOOD, CHANGE_PARAM_BAD):
        uav_query(op)
    else:
        print("ERROR INPUT!")

def uav_query(op):
    msg = {CMD: op}
    for uav in g_conn_pool.values():
        msg['time'] = time.time()
        uav.sendall(json.dumps(msg).encode(encoding='utf8'))


def cal_G_U():
    msg = {CMD: CAL_DIST_G_U}
    while True:
        uav_name = input('input client_name：')
        if uav_name == '-1':
            break
        uav = g_conn_pool.get(uav_name)
        if uav is None:
            print('No such uav!')
            continue
        msg[TIME] = time.time()
        uav.sendall(json.dumps(msg).encode(encoding='utf8'))
        break

def cal_2_uavs():
    count = 0
    msg = {CMD: CAL_DIST_2UAV}
    while True:
        if count == 2:
            break
        uav_name = input('\n input client_name：')
        if uav_name == '-1':
            break
        uav = g_conn_pool.get(uav_name)
        if uav is None:
            print('No such uav!')
            continue
        count += 1
        msg[TIME] = time.time()
        uav.sendall(json.dumps(msg).encode(encoding='utf8'))


def set_ground_location(command):
    msg = {CMD: command}
    while True:
        uav_name = input('input client_name：')
        if uav_name == '-1':
            break
        uav = g_conn_pool.get(uav_name)
        if uav is None:
            print('No such uav!')
            continue
        msg[TIME] = time.time()
        uav.sendall(json.dumps(msg).encode(encoding='utf8'))
        break


def multi_uav_fly():
    message = {}
    while True:
        uav_name = input('input client_name(-1 end input)：')
        if uav_name == '-1':
            break
        uav = g_conn_pool.get(uav_name)
        if uav is None:
            print('No such uav!')
            continue
        data = data_input()
        msg = {CMD: UAV_FLY, 'data': data}
        message[uav] = msg
    for uav, msg in message.items():
        msg['time'] = time.time()
        uav.sendall(json.dumps(msg).encode(encoding='utf8'))






def all_uavs_fly():
    data = data_input()
    msg = {CMD: UAV_FLY, 'data': data}
    for uav in g_conn_pool.values():
        msg['time'] = time.time()
        uav.sendall(json.dumps(msg).encode(encoding='utf8'))

def data_input():
    while True:
        strvar = input("input instruction(x:,y:,z:,duration: ):")
        plain = strvar
        strvar = strvar.split(' ')
        if (len(strvar) == 1 and plain.upper() != 'Q' and plain.upper() != 'L' and plain.upper() != 'F') or (
                len(strvar) != 1 and len(strvar) != 4):
            print("wrong input\n")
            continue
        break
    return plain


def time_test(client_name, uav):
    file_names = 'test_'
    file_count = 10
    for i in range(file_count):
        total = 100
        file_name = file_names + str(i+1)
        for j in range(total):
            t = time.time()
            msg = {'cmd': TIME_TEST, 'index': j, TIME: t, 'total': total, 'file': file_name, 'client_name': client_name}
            uav.sendall(json.dumps(msg).encode('utf-8'))
            time.sleep(1)


def send_ground_location():
    msg = {CMD: SEND_GROUND_LOCATION, LAT: ground_lat, LON: ground_lon, ALT: ground_alt}
    while True:
        uav_name = input('input client_name(-1 end input, all send to all UAVs )：')
        if uav_name == 'all':
            for uav in g_conn_pool.values():
                msg[TIME] = time.time()
                uav.sendall(json.dumps(msg).encode(encoding='utf8'))
            break
        if uav_name == '-1':
            break
        uav = g_conn_pool.get(uav_name)
        if uav is None:
            print('No such uav!')
            continue
        msg[TIME] = time.time()
        uav.sendall(json.dumps(msg).encode(encoding='utf8'))

def set_g_l():
    # 从输入设置地面站的经纬度
    global ground_lat, ground_lon, ground_alt
    ground_lat = float(input('请输入lat：'))
    ground_lon = float(input('请输入lon: '))
    ground_alt = float(input('请输入alt: '))

# def task_c():
#     uav01 = g_conn_pool.get('uav01')
#     uav02 = g_conn_pool.get('uav02')

#     msg1 = {CMD:UAV_FLY, 'data': '1 0 0 1'}
#     msg1['time'] = time.time()
#     uav01.sendall(json.dumps(msg1).encode(encoding='utf8'))

#     msg2 = {CMD:UAV_FLY, 'data': '1 0 0 1'}
#     msg2['time'] = time.time()
#     uav02.sendall(json.dumps(msg2).encode(encoding='utf8'))

def task1_1():
    uav01 = g_conn_pool.get('uav01')
    uav02 = g_conn_pool.get('uav02')
    uav03 = g_conn_pool.get('uav03')
    uav04 = g_conn_pool.get('uav04')


    msg1 = {CMD: UAV_FLY, 'data': '60 0 0 0'}
    msg1['time'] = time.time()
    uav01.sendall(json.dumps(msg1).encode(encoding='utf8'))
    

    msg2 = {CMD: UAV_FLY, 'data': '60 0 0 0'}
    msg2['time'] = time.time()
    uav02.sendall(json.dumps(msg2).encode(encoding='utf8'))

    msg3 = {CMD: UAV_FLY, 'data': '60 0 0 0'}
    msg3['time'] = time.time()
    uav03.sendall(json.dumps(msg3).encode(encoding='utf8'))

    msg4 = {CMD: UAV_FLY, 'data': '60 0 0 0'}
    msg4['time'] = time.time()
    uav04.sendall(json.dumps(msg4).encode(encoding='utf8'))

def task1_2():
    uav01 = g_conn_pool.get('uav01')
    uav02 = g_conn_pool.get('uav02')
    uav03 = g_conn_pool.get('uav03')
    uav04 = g_conn_pool.get('uav04')


    msg1 = {CMD: UAV_FLY, 'data': '0 5 0 0'}
    msg1['time'] = time.time()
    uav01.sendall(json.dumps(msg1).encode(encoding='utf8'))
    

    msg2 = {CMD: UAV_FLY, 'data': '0 5 0 0'}
    msg2['time'] = time.time()
    uav02.sendall(json.dumps(msg2).encode(encoding='utf8'))

    msg3 = {CMD: UAV_FLY, 'data': '0 5 0 0'}
    msg3['time'] = time.time()
    uav03.sendall(json.dumps(msg3).encode(encoding='utf8'))

    msg4 = {CMD: UAV_FLY, 'data': '0 5 0 0'}
    msg4['time'] = time.time()
    uav04.sendall(json.dumps(msg4).encode(encoding='utf8'))

def task1_3():
    uav01 = g_conn_pool.get('uav01')
    uav02 = g_conn_pool.get('uav02')
    uav03 = g_conn_pool.get('uav03')
    uav04 = g_conn_pool.get('uav04')


    msg1 = {CMD: UAV_FLY, 'data': '-60 0 0 0'}
    msg1['time'] = time.time()
    uav01.sendall(json.dumps(msg1).encode(encoding='utf8'))
    

    msg2 = {CMD: UAV_FLY, 'data': '-60 0 0 0'}
    msg2['time'] = time.time()
    uav02.sendall(json.dumps(msg2).encode(encoding='utf8'))

    msg3 = {CMD: UAV_FLY, 'data': '-60 0 0 0'}
    msg3['time'] = time.time()
    uav03.sendall(json.dumps(msg3).encode(encoding='utf8'))

    msg4 = {CMD: UAV_FLY, 'data': '-60 0 0 0'}
    msg4['time'] = time.time()
    uav04.sendall(json.dumps(msg4).encode(encoding='utf8'))

def task1_4():
    uav01 = g_conn_pool.get('uav01')
    uav02 = g_conn_pool.get('uav02')
    uav03 = g_conn_pool.get('uav03')
    uav04 = g_conn_pool.get('uav04')


    msg1 = {CMD: UAV_FLY, 'data': '0 -5 0 0'}
    msg1['time'] = time.time()
    uav01.sendall(json.dumps(msg1).encode(encoding='utf8'))
    

    msg2 = {CMD: UAV_FLY, 'data': '0 -5 0 0'}
    msg2['time'] = time.time()
    uav02.sendall(json.dumps(msg2).encode(encoding='utf8'))

    msg3 = {CMD: UAV_FLY, 'data': '0 -5 0 0'}
    msg3['time'] = time.time()
    uav03.sendall(json.dumps(msg3).encode(encoding='utf8'))

    msg4 = {CMD: UAV_FLY, 'data': '0 -5 0 0'}
    msg4['time'] = time.time()
    uav04.sendall(json.dumps(msg4).encode(encoding='utf8'))

def taskf():
    task1_1()
    time.sleep(10)
    task1_2()
    time.sleep(3)
    task1_3()
    time.sleep(10)
    task1_4()






if __name__ == '__main__':
    init()
    # 新开一个线程，用于接收新连接
    thread = Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()
    # 主线程逻辑
    while True:
        op = input('input operation:')
        send_data(op)

