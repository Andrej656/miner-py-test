import json

def construct_message(data):
    # Convert data to JSON format for simplicity (actual implementation might differ)
    message = json.dumps(data)
    # Add length prefix to the message to indicate its size
    return f"{len(message):<10}" + message.encode()

def parse_message(message):
    # Extract the length prefix to determine the size of the message
    length_prefix = int(message[:10].strip())
    # Extract the actual message content based on the determined length
    message_content = message[10:length_prefix + 10]
    return json.loads(message_content)
