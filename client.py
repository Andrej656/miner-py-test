import socket


class StratumV2Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.socket.connect((self.server_ip, self.server_port))
            print("Connected to server")
        except ConnectionRefusedError:
            print("Connection refused")

    def send_request(self, request_data):
        # Construct and send Stratum V2 request
        message = utils.construct_message({"type": constants.MESSAGE_TYPE_REQUEST, "data": request_data})
        self.socket.send(message)

    def receive_response(self):
        # Receive and process Stratum V2 response
        response = self.socket.recv(constants.MAX_RESPONSE_SIZE)
        parsed_response = utils.parse_message(response)
        return parsed_response

    def close(self):
        self.socket.close()
