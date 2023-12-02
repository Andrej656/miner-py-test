import socket
from .common import constants
from .common import utils

class StratumV2Server:
    def __init__(self, listen_ip, listen_port):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def start(self):
        self.socket.bind((self.listen_ip, self.listen_port))
        self.socket.listen(constants.MAX_CONNECTIONS)
        print("Server listening on", self.listen_ip, "port", self.listen_port)

        while True:
            client_socket, addr = self.socket.accept()
            print("Connection from", addr)
            self.clients.append(client_socket)
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        try:
            while True:
                # Receive and process Stratum V2 request
                request = client_socket.recv(constants.MAX_RESPONSE_SIZE)
                if not request:
                    break  # Break the loop if no data is received
                parsed_request = utils.parse_message(request)
                # Process the request and generate a response
                response_data = self.process_request(parsed_request["data"])
                # Send the response back to the client
                self.send_response(client_socket, response_data)
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def send_response(self, client_socket, response_data):
        # Construct and send Stratum V2 response to the client
        message = utils.construct_message({"type": constants.MESSAGE_TYPE_RESPONSE, "data": response_data})
        client_socket.send(message)

    def process_request(self, request_data):
        # Process the received request data and generate a response
        # For simplicity, this just echoes the received data
        return {"response": "Received: " + str(request_data)}

    def stop(self):
        for client_socket in self.clients:
            client_socket.close()
        self.socket.close()
