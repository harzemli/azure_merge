import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 4242
buffer_size = 1024

# connect to first client (Godot)
godot_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
godot_sock.bind((UDP_IP, UDP_PORT))
while True:
    godot_data, godot_address = godot_sock.recvfrom(buffer_size)
    if godot_data:
        print("received message socket 1:", godot_data)
        break

# connect to second client (Raspberry Pi)
pi_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
pi_sock.bind((UDP_IP, 4243))
while True:
    pi_data, pi_address = pi_sock.recvfrom(buffer_size)
    if pi_data:
        print("received message socket 2:", pi_data)
        break

while True:
    # Data received from the Raspberry Pi
    msg_from_pi, pi_address = pi_sock.recvfrom(1024)
    print("Received from Pi: " + msg_from_pi.decode("utf-8"))

    # Data sent to Godot
    godot_sock.sendto(msg_from_pi, godot_address)

    # Data sent to the Raspberry Pi
    msg = "Received from internal communications manager: " + str(time.time())
    pi_sock.sendto(msg.encode("utf-8"), pi_address)
