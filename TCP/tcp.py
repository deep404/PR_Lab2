# Importing all needed libraries.
import socket
import json
from db_manager import DataBaseManager

# Setting the host and port of the tcp server.
HOST = '127.0.0.1'
PORT = 65432

# Creating the server.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Binding to the TCP host and port.
    s.bind((HOST, PORT))

    # Setting into the listening mode.
    s.listen()

    # Getting the connection and address objects.
    conn, addr = s.accept()
    with conn:
        while True:
            # Getting the data from the tcp request.
            data = conn.recv(1024)
            if data:
                # Converting the data from binary to json.
                string_data = data.decode()
                json_data = json.loads(string_data)

                # Getting the remainder name, body and time.
                remainder_name = json_data["remainder-name"]
                remainder_body = json_data["remainder-body"]
                remainder_time = json_data["remainder-time"]

                # Saving the remainder data to the data base.
                database_manager = DataBaseManager('database.db')
                database_manager.add_remainder(remainder_name, remainder_body, remainder_time)
                database_manager.close()

                # Creating the response message.
                message = {"status" : "done"}
                message_binary = json.dumps(message).encode()

                # Sending the message to the server back.
                conn.sendall(message_binary)
