# Importing all needed libraries.
import json
from flask import Flask, jsonify, request
import smtplib, ssl
import socket

# Creating the flask application.
app = Flask(__name__)

# Email settings.
EMAIL = 'test.pr.labs@gmail.com'
PASSWORD = 'pr_lab_com_faf192'
EMAIL_PORT = 465

ssl_context = ssl.create_default_context()

# Remainder functionality settings.
TCP_HOST = '127.0.0.1'
TCP_PORT = 65432

# Task functionality settings.
UDP_SERTVER_HOST_PORT = ('127.0.0.1', 4546)

@app.route('/', methods= ['POST', 'GET'])
def index():
    if request.method == 'GET':
        # Getting the sent data to the server.
        json_data = request.json

        if json_data['type'] == 'send-email':
            # Getting the the receiver and the body of the email to be send.
            receiver_email = json_data['body']['receiver-email']
            email_message = json_data['body']['email-message']

            # Log in and sending the email to the receiver.
            with smtplib.SMTP_SSL("smtp.gmail.com", EMAIL_PORT, context=ssl_context) as server:
                server.login(EMAIL, PASSWORD)
                server.sendmail(EMAIL, receiver_email, email_message)
        elif json_data['type'] == 'add-remainder':
            # Getting the remainder data to send to the remainder creation server.
            tcp_body = json_data['body']
            tcp_body_binary = json.dumps(tcp_body).encode()

            # Connecting to the remainder creation server, sending the TCP request and getting the status.
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((TCP_HOST, TCP_PORT))
                s.sendall(tcp_body_binary)
                data_back = s.recv(1024)
                data_back_json = json.loads(data_back.decode())
                return jsonify(data_back_json)

        elif json_data['type'] == 'add-task':
            # Getting the remainder data to send to the task creation server.
            udp_body = json_data['body']
            udp_body_binary = json.dumps(udp_body).encode()

            # Connecting to the task creation server, sending the TCP request and getting the status.
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_server:
                udp_server.sendto(udp_body_binary, UDP_SERTVER_HOST_PORT)
                data_back = udp_server.recvfrom(1024)[0]
                data_back_json = json.loads(data_back.decode())
                return jsonify(data_back_json)
    return ''

# Running the main app.
app.run()