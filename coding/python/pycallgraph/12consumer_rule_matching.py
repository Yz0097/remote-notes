import os
import requests
from kafka import KafkaConsumer
import json
import time
import re
import socket
from request import get_and_compare_hash, get_file

consumer = KafkaConsumer('audit_logs', 
                         bootstrap_servers='192.168.10.205:9092', 
                         auto_offset_reset='latest',
                         )

ip_pattern = re.compile(r'((\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]):(6[0-5]{2}[0-3][0-5]|[1-5]\d{4}|[1-9]\d{1,3}|[0-9]))')

url = "http://192.168.10.236:8080/get"  # need to update the url
model = get_and_compare_hash(url, "uav07","rules.zip")
if not model:
    print("rules file is not correct, program exit.")
    if not get_file(url,"uav07","rules.zip"): exit(0)
else:
    os.system('unzip rules.zip')

print("get model from blockchain successfully!")

rules = [] # normal syscall
with open("./rules/rules-normal-kind.txt") as f1:
    rules = f1.readlines()

ips = [] # normal ip list
with open("./rules/ips.txt") as f2:
    ips = f2.readlines()
ips = [ip[:-1] for ip in ips] # remove "\n"

normal_count_dict = {} # normal syscall count num
with open("./rules/rules-count.txt") as f3:
    normal_count_dict = json.loads(f3.read())

current_tms = round(time.time())
file_name = f"./data/abnormal_{current_tms}_uav7.json"
f = open(file_name, "w", encoding="utf-8")
file_name = f"./data/attack_{current_tms}_uav7.json"
f1 = open(file_name, "w", encoding="utf-8")

count_dict = {} # count every syscall and compare them with threshold

#发送接口1需要参数
def send_udp_message1(num1,num5):
    # 创建一个新的 UDP socket
    target_ip = "192.168.10.245"
    target_port = 9101
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #message0 = f"{num1} {num2} {num3} {num4} {num5}"
    message0 = f"{num1} {num5}"
    udp_socket.sendto(message0.encode(), (target_ip, target_port))

#发送接口2需要参数
aBType = 0
def send_udp_message2(num1,num2,num3,num4,num5):
    # 创建一个新的 UDP socket
    target_ip1 = "192.168.10.245"
    target_port1 = 9102
    udp_socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    num21 = namematch(num2)
    message1 = f"{num1}+{num21}+{num3}+{num4}+{num5}"
    #message1 = f"{num1}+{num2}+{num3}+{num4}"
    udp_socket1.sendto(message1.encode(), (target_ip1, target_port1))

    with open('exception_log.txt', 'a+') as file:
        file.seek(0, 2)
        log_message = f'{num4}\n'
        file.write(log_message)

def namematch(num):
    if str(num) == "5522d5aeebeb":
        x = f"飞控任务容器"
    else:
        x = f"飞控任务容器"
    return x

def send_udp_message_keti5(uavid, event):
    json.dump(event, f1, indent=2)
    f1.write(",\n") # save attack json file
    # data = {
    #     "uavid": uavid,
    #     "event": event
    # }
    # headers = {
        # "Content-Type", "application/json"
    # }
    # url = "http://localhost:8080"
    # response = requests.post(url=url, headers=headers, data=data)
    print("send current anomaly log to keti5 successfully.")

for msg in consumer:
    try:
        aBType = 0
        uavid = 'uav07'
        log = b"{" + msg.value.split(b"{")[1]
        event = json.loads(log)
        # detect anomaly camera behavior
        if event['container_name'] == "fervent_cray":
            if not event['source-name'] in count_dict.keys():
                count_dict[event['source-name']] = 0
            else:
                count_dict[event['source-name']] += 1

            if event['source-name'] in normal_count_dict.keys(): # compare with normal syscall count
                syscall_num_thre = normal_count_dict[event['source-name']] * 2
                if count_dict[event['source-name']] >= syscall_num_thre:
                    aBType = 1
                    timestamp = int(time.time())
                    
                    sevent=f"{event['source-name']} -> {event['edge-type']} -> {event['destination-name']}"
                    send_udp_message2(uavid,event['container_id'], timestamp, aBType, sevent) #发送接口2
                    print("****camera behavior error.")
                    print("camera err log: ", event)

        # detect new anomaly syscall which not in rules
        if "->" in event['destination-name']:
            string = event['destination-name']
            event['destination-name'] = string.split("->")[0].split(":")[0] + "->" + string.split("->")[1].split(":")[0]
        elif ":" in event['destination-name']:
            string = event['destination-name']
            event['destination-name'] = string.split(":")[0]
        behavior = event['source-name'] + "->" + event['edge-type'] + "->" + event['destination-name'] + "\n"
        if not behavior in rules:
            aBType = 2
            timestamp = int(time.time())
            
            sevent=f"{event['source-name']} -> {event['edge-type']} -> {event['destination-name']}"
            send_udp_message2(uavid,event['container_id'], timestamp, aBType, sevent) #发送接口2
            #send_udp_message_keti5(uavid, event)
            print("****error behavior: ", behavior)
            send_udp_message1(uavid, 100) #发送接口1所需准确率

        # detect anomaly ip address
        ip_list = ip_pattern.findall(event['destination-name'])
        if len(ip_list) != 0:
            for ip in ip_list:
                ip = ip[0].split(":")[0] # drop random port, only focus on ip
                if not ip in ips:
                    aBType = 3
                    timestamp = int(time.time())

                    sevent=f"{event['source-name']} -> {event['edge-type']} -> {event['destination-name']}"
                    send_udp_message2(uavid,event['container_id'], timestamp, aBType, sevent) #发送接口2
                    #send_udp_message_keti5(uavid, event)
                    print("****error external ip address in/out: ", ip)
                    print("error process log: ", event)
                    send_udp_message1(uavid, 100) #发送接口1所需准确率


        json.dump(event, f, indent=2)
        f.write(",\n")

        #timestamp = int(time.time())
        #send_udp_message2(1, timestamp, aBType, event) #发送接口2所需准确率

    except (ValueError, IndexError) as e:
        print("the data is not json format. continue...")
        continue
f1.close()
f.close()
