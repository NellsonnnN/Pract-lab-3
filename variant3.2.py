import socket
import json
from datetime import datetime
import os

def connect_to_server():
    server_address = ('localhost', 12345)  # Укажите необходимый адрес и порт
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    return client_socket


def send_request_and_receive_data(client_socket):
    client_socket.sendall(b"Request for process info")
    data = b""
    while True:
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        data += chunk

    updated_process_info = json.loads(data.decode('utf-8'))
    return updated_process_info


def update_and_save():
    client_socket = connect_to_server()
    updated_process_info = send_request_and_receive_data(client_socket)
    update_time_str = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")
    update_path = f"./{update_time_str}"
    os.makedirs(update_path, exist_ok=True)
    with open(f"{update_path}/updated_process_info.json", 'w') as json_file:
        json.dump(updated_process_info, json_file, indent=2)
    client_socket.close()


if __name__ == "__main__":
    command = input("Enter command: ")
    if command.lower() == "update":
        update_and_save()
    else:
        print("Invalid command. Please enter 'update' to update the file.")
