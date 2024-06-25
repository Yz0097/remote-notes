import socket
import json
from pymavlink import mavutil
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import csv
from threading import Thread
from geopy.distance import geodesic
import datetime
import subprocess
import math


client_name = 'xwq'
UAV_WARN = 'WARN'
UAV_END = 'END'
UAV_FLY = 'FLY'
CMD = 'cmd'

TIME_TEST = 'delay_time'
LAT = 'lat'
LON = 'lon'
ALT = 'alt'
TIME = 'time'

SEND_GROUND_LOCATION = 'send_g_l'
GET_UAV_LOCATION = 'set_g_l'
SET_G_LOCATION = 'set_g_l'
CAL_DIST_2UAV = 'cal_uavs'
CAL_DIST_G_U = 'dist_uav'
QUERY_BATTERY = 'battery'
UAV_INFO = 'uav_info'
SEND_DATA = 'send_data'

# Drone Fix CMD
CHANGE_PARAM_BAD = 'bad'
CHANGE_PARAM_GOOD = 'good'

SUCCESS = 'success'
CONNECT = 'connect'

ground_lat = 30.28708
ground_lon = 120.12802999999997
ground_alt = 40.23141


def send_body_ned_velocity(vehicle, velocity_x, velocity_y, velocity_z):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, # frame Needs to be MAV_FRAME_BODY_NED for forward/back left/right control.
        0b010111111000, # type_mask（Position）0b110111000111(Velocity)
        #0b0000111111111000, # type_mask (only positions enabled)
        #0b0000111111000111, # type_mask (only speeds enabled)
        velocity_x, velocity_y, velocity_z, # m/s
        0, 0, 0, # x, y, z positions (not used)
        0, 0, 0, # x, y, z acceleration
        0, 0)
    vehicle.send_mavlink(msg)

    
# def send_body_ned_velocity(vehicle, velocity_x, velocity_y, velocity_z, duration=0):
#     msg = vehicle.message_factory.set_position_target_global_int_encode(
#         0,       # time_boot_ms (not used)
#         0, 0,    # target system, target component
#         mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame Needs to be MAV_FRAME_BODY_NED for forward/back left/right control.
#         #0b110111111000, # type_mask（Position）0b110111000111(Velocity)
#         #0b0000111111111000, # type_mask (only positions enabled)
#         0b0000111111000111, # type_mask (only speeds enabled)
#         0, 0, 0, # x, y, z positions (not used)
#         velocity_x, velocity_y, velocity_z, # m/s
#         0, 0, 0, # x, y, z acceleration
#         0, 0)
#     for x in range(0,duration):
#         vehicle.send_mavlink(msg)
#         time.sleep(1)
#     # send command to vehicle
    #vehicle.send_mavlink(msg)

# def send_body_ned_velocity2(vehicle, velocity_x, velocity_y, velocity_z, duration=0):
#     msg = vehicle.message_factory.set_position_target_local_ned_encode(
#         0,       # time_boot_ms (not used)
#         0, 0,    # target system, target component
#         mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame Needs to be MAV_FRAME_BODY_NED for forward/back left/right control.
#         #0b110111111000, # type_mask（Position）0b110111000111(Velocity)
#         0, 0, 0, # x, y, z positions (not used)
#         velocity_x, velocity_y, velocity_z, # m/s
#         0, 0, 0, # x, y, z acceleration
#         0, 0)
#     for x in range(0,duration):
#         vehicle.send_mavlink(msg)
#         time.sleep(1)

# def send_body_ned_velocity3(vehicle, velocity_x, velocity_y, velocity_z, duration=0):
#     msg = vehicle.message_factory.set_position_target_local_ned_encode(
#         0,       # time_boot_ms (not used)
#         0, 0,    # target system, target component
#         mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, # frame Needs to be MAV_FRAME_BODY_NED for forward/back left/right control.
#         #0b110111111000, # type_mask（Position）0b110111000111(Velocity)
#         0, 0, 0, # x, y, z positions (not used)
#         velocity_x, velocity_y, velocity_z, # m/s
#         0, 0, 0, # x, y, z acceleration
#         0, 0)
#     for x in range(0,duration):
#         vehicle.send_mavlink(msg)
#         time.sleep(1)


def fly_height(vehicle, takeoff_alt):
    while not vehicle.is_armable:
        time.sleep(1)
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    while not vehicle.armed:
        print('Waiting for arming...')
        time.sleep(1)
    vehicle.simple_takeoff(takeoff_alt)  # Take off to target altitude
    while True:
        print('Altitude: %d' % vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= takeoff_alt * 0.95:
            print('REACHED TARGET ALTITUDE')
            break
        time.sleep(1)


def send_data(client, cmd, uav_info):
    msg = {CMD: cmd, 'client_name': client_name, 'uav_info': uav_info}
    msg[TIME] = time.time()
    client.sendall(json.dumps(msg).encode('utf8'))


def input_client_name():
    return input("please input uav name :")


def cal_dist(uav_lat, uav_lon, uav_alt):
    l_dist = geodesic((ground_lat, ground_lon), (uav_lat, uav_lon)).meters
    h_dist = ground_alt - uav_alt
    dist = math.sqrt(l_dist * l_dist + h_dist * h_dist)
    print('distance between Ground and uav: %lf' % dist)
    return dist


def sock_client_data(vehicle, msg, fly_in_air):
    dec_msg = msg
    if not fly_in_air and dec_msg.upper() == "F":
        print('takeoff!!!')
        takeoff_alt = 3
        fly_height(vehicle, takeoff_alt)
        return UAV_FLY
    if fly_in_air and dec_msg.upper() == "F":
        print('uav is in the air! Dot need to takeoff again!')
        return UAV_WARN
    if not fly_in_air and dec_msg.upper() != 'F':
        print('please let uav takeoff firstly !')
        return UAV_WARN
    if dec_msg.upper() == "L":
        print("start land")
        vehicle.mode = VehicleMode("LAND")
        return UAV_END

    dec_msg = dec_msg.split(' ')
    # print(dec_msg)
    velocity_x = int(dec_msg[0])
    velocity_y = int(dec_msg[1])
    velocity_z = int(dec_msg[2])
    duration = int(dec_msg[3])
    # print(duration)
    #if velocity_x > 3 or velocity_y > 3 or velocity_z > 3:
        #print("Too fast\n")
        #return UAV_WARN
   # if duration > 10:
      # print("Too long\n")
      # return UAV_WARN
    print('execute instruction:' + msg)
    send_body_ned_velocity(vehicle, velocity_x, velocity_y, velocity_z)

    #time.sleep(duration)


def network_test(HOST, vehicle):
    count = 0
    lose_packet = 3
    time_re = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    while (True):
        status, info = subprocess.getstatusoutput('ping -c 1 ' + HOST)
        if status == 0:
            count = 0
            continue
            # time_re = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # print("OK,%s" % time_re)

            # return True
        else:
            count += 1
            if count == lose_packet:
                time_re = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # print(time_re)

            print('第 %d 次 LOSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS' % count)
            if count > lose_packet:
                break
        time.sleep(0.5)

    # 获取无人机经纬度
    uav_lat, uav_lon, uav_alt = get_local(vehicle)
    # uav_lat, uav_lon ,uav_alt= 28.7427, 115.86572000000001, 34.213213

    # land
    vehicle.mode = VehicleMode("LAND")

    discon_dist = cal_dist(uav_lat, uav_lon, uav_alt)

    # record info
    with open('./log.txt', 'a') as f:
        f.write('第 %d 次 LOSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS\n' % count)
        f.write('time:%s\n' % time_re)
        f.write('LANDDDDDDDDDDDDDDDDDDDDDDDD\n')
        f.write(" uav_lat: %lf , uav_lon: %lf, uav_alt: %lf \n" % (uav_lat, uav_lon, uav_alt))
        f.write(" ground_lat: %lf , ground_lon: %lf, ground_alt: %lf \n" % (ground_lat, ground_lon, ground_lat))
        f.write(' disconnect_distance: %lf \n' % discon_dist)


def get_local(vehicle):
    location = vehicle.location.global_frame
    uav_lat, uav_lon, uav_alt = location.lat, location.lon, location.alt
    # uav_lat, uav_lon, uav_alt = 28.7427, 115.86572000000001, 425.2134
    return uav_lat, uav_lon, uav_alt

def record_ground_location(lat, lon, alt):
    global ground_lat, ground_lon, ground_alt
    ground_lat, ground_lon, ground_alt = lat, lon, alt
    print('set_ground: lat : %lf, lon: %lf, alt: %lf' % (ground_lat, ground_lon, ground_alt))


def send_uav_location(vehicle, command):
    uav_lat, uav_lon, uav_alt = get_local(vehicle)
    t = time.time()
    send_msg = {CMD: command, LAT: uav_lat, LON: uav_lon, ALT: uav_alt, TIME: t, 'client_name': client_name}
    client.sendall(json.dumps(send_msg).encode('utf8'))

def change_param_bad(vehicle, client):
    """
    改参数
    """
    vehicle.parameters['INS_POS1_Z'] = -0.3
    vehicle.parameters['INS_POS2_Z'] = -0.3
    uav_info = 'change parameter: INS_POS1_Z : %lf, INS_POS2_Z: %lf' % (-0.3, -0.3)
    send_data(client, SEND_DATA, uav_info)


def change_param_good(vehicle, client):
    """
    恢复
    """
    vehicle.parameters['INS_POS1_Z'] = 0
    vehicle.parameters['INS_POS2_Z'] = 0
    uav_info = 'change parameter: INS_POS1_Z : %lf, INS_POS2_Z: %lf' % (0, 0)
    send_data(client, SEND_DATA, uav_info)

def query_battery(vehicle, client):
    battery = vehicle.battery
    uav_info = " Battery: %s" % battery
    send_data(client, SEND_DATA, uav_info)


if '__main__' == __name__:
    HOST = '192.168.1.100'  # 比如 99.100.101.102是你的服务器的公网IP
    PORT = 8712  # IP开放的socket端口
    ADDR = (HOST, PORT)

    client_name = input_client_name()
    client = socket.socket()
    client.connect(ADDR)
    print(client.recv(2048).decode(encoding='utf8'))
    send_data(client, CONNECT, 'success')

    connection_string = '/dev/ttyACM0'  # Edit to suit your needs.   real
    # connection_string = '127.0.0.1:14551'
    vehicle = connect(connection_string, wait_ready=True)
    # vehicle = '123'

    # thread to test distance
    # thread = Thread(target=network_test, args=(HOST, vehicle))
    # thread.setDaemon(True)
    # thread.start()

    fly_in_air = False
    delay_list = []
    # 接受消息
    while True:
        try:
            rec = client.recv(2048).decode(encoding='utf8')
            rec_time = time.time()
            msg = json.loads(rec)
            delay_time = (rec_time - msg[TIME]) * 1000
            # print('delay time: ' + str(delay_time) + ' ms')
            command = msg[CMD]

            if command == TIME_TEST:
                client.sendall(json.dumps(msg).encode('utf8'))

            elif command == SEND_GROUND_LOCATION:
                record_ground_location(msg[LAT], msg[LON], msg[ALT])

            elif command in (CAL_DIST_2UAV, SET_G_LOCATION, CAL_DIST_G_U):
                send_uav_location(vehicle, command)

            elif command == UAV_FLY:
                instruction = msg['data']
                if instruction.upper() == "Q" and not fly_in_air:
                    break
                flag = sock_client_data(vehicle, instruction, fly_in_air)
                if flag == UAV_END:
                    break
                elif flag == UAV_FLY:
                    fly_in_air = True
                elif flag == UAV_WARN:
                    continue
            # Drone Fix
            elif command == CHANGE_PARAM_BAD:
                change_param_bad(vehicle, client)

            elif command == CHANGE_PARAM_GOOD:
                change_param_good(vehicle, client)
            elif command == QUERY_BATTERY:
                query_battery(vehicle, client)

        except Exception as e:
            print(e)
            break



