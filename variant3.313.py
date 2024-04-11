import os
import json
import psutil
from datetime import datetime
import socketserver


def collect_process_info():
    process_info = []
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        process_info.append({
            'pid': process.info['pid'],
            'name': process.info['name'],
            'cpu_percent': process.info['cpu_percent']
        })
    return process_info


class ProcessInfoRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        process_info = collect_process_info()
        current_time_str = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")
        file_path = f"./{current_time_str}/process_info.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        save_process_info_to_file(process_info, file_path)

        with open(file_path, 'r') as json_file:
            data = json_file.read()

        self.request.sendall(data.encode('utf-8'))


def save_process_info_to_file(process_info, file_path):
    json_data = json.dumps(process_info, indent=2)
    with open(file_path, 'w') as json_file:
        json_file.write(json_data)


if __name__ == "__main__":
    server_address = ('localhost', 12345)  # Укажите необходимый адрес и порт
    server = socketserver.TCPServer(server_address, ProcessInfoRequestHandler)
    print("Server is running...")
    server.serve_forever()
