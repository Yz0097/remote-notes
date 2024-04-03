import socket
import serial



udp_ip = "0.0.0.0"  # 监听全部网络接口
udp_port = 8715  # UDP 服务端口号

serial_port = '/dev/ttyACM0'  # 串口名称
serial_baudrate = 9600  # 串口波特率

# 创建 UDP 套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定套接字到指定的 IP 地址和端口号
sock.bind((udp_ip, udp_port))
print(f"UDP 服务已启动，监听端口 {udp_port}")

# 打开串口
ser = serial.Serial(serial_port, serial_baudrate)
print(f"已打开串口 {serial_port}")



while True:
    # 接收 UDP 数据报
    data, addr = sock.recvfrom(1024)
    print(f"接收到来自 {addr} 的数据: {data}")

    # 将接收到的报文转发至串口
    ser.write(data)
    print("数据已转发至串口")
