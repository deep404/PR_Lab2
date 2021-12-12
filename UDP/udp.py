# Importing all needed libraries.
import socket
import json
from db_manager import DataBaseManager

# Setting the host and the port of the UDP server.
HOST = '127.0.0.1'
PORT = 4546

# Creating the server.
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_server:
    # Binding to the UDP server.
    udp_server.bind((HOST, PORT))

    while True:
        # Getting the UDP request from the server.
        data = udp_server.recvfrom(1024)

        if data:
            # Getting the message from the UDP request and converting it into a json format.
            message = data[0].decode()
            json_data = json.loads(message)

            # Getting the task's name, body and the due date.
            task_name = json_data["task-name"]
            task_body = json_data["task-body"]
            task_due_date = json_data["task-due-date"]

            # Creating the data base and saving the new task.
            database_manager = DataBaseManager('database.db')
            database_manager.add_task(task_name, task_body, task_due_date)
            database_manager.close()

            # Creating the response message.
            message = {"status" : "done"}
            message_binary = json.dumps(message).encode()

            # Sending the message to the server back.
            udp_server.sendto(message_binary, data[1])

