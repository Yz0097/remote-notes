from dronekit import connect
import socket
from threading import Event

# 连接到无人机飞控
vehicle = connect('/dev/ttyACM0', wait_ready=True)

# 创建 TCP Socket 对象
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 服务器地址和端口
server_address = ('192.168.10.201', 8713)  # 将 '服务器IP地址' 更改为实际的服务器 IP 地址

# 连接服务器
tcp_socket.connect(server_address)

# 发送数据给服务器
message = "Hello, server!"
tcp_socket.sendall(message.encode())

# 定义一个回调函数来处理接收到的消息
try:
    # 创建一个事件对象
    message_processed_event = Event()
    def handle_mavlink_v2_message(vehicle, name, message):
        #print('接收到 mavlink v2 消息:', message)
        if message:
            tcp_socket.send(message.get_msgbuf())  # 发送数据到服务器

    # 注册回调函数来处理 MAVLink v2 消息
    vehicle.add_message_listener('*', handle_mavlink_v2_message)
    # 主线程等待事件被设置
    message_processed_event.wait()
except KeyboardInterrupt:
    print('接收到键盘中断，停止转发')

finally:
    # 关闭连接
    tcp_socket.close()
    vehicle.close()
