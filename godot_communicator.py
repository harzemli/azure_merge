import socket
import time
import threading


class Connection:
    timestamp = time.time()
    text = ""

    def __init__(self, ip: str, listener_port: int):
        self.godot_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.godot_socket.bind((ip, listener_port))
        print("waiting for client")
        data, self.godot_address = self.godot_socket.recvfrom(1024)
        print("received message:", data)
    
    def receive_data(self):
        try:
            self.godot_socket.settimeout(0.0001)
            data, adder = self.godot_socket.recvfrom(1024)

            # interval = time.time() - Connection.timestamp
            # print(1/interval)
            # Connection.timestamp = time.time()

            return data
        except socket.timeout:
            return
    
    def send_data(self, update_interval):
        while self.text == "":
            pass
        while True:
            start_time = time.time()
            self.godot_socket.sendto(self.text.encode('utf-8'), self.godot_address)
            sleep_time = update_interval - (time.time() - start_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    def start_sending(self, update_interval):
        sender = threading.Thread(target=self.send_data, args=(update_interval,), daemon=True)
        sender.start()
        return
    
    def set_data(self, text):
        self.text = text
