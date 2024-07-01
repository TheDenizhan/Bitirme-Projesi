import cv2
import socket
import pickle
import struct

# Initialize socket connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.103', 5000))

data = b""
payload_size = struct.calcsize("L")

while True:
    # Receive frame size
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024)
        if not packet: break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]

    # Unpack frame size
    msg_size = struct.unpack("L", packed_msg_size)[0]

    # Receive frame data
    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Deserialize frame
    frame = pickle.loads(frame_data)

    # Display frame
    cv2.imshow('Received', frame)
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()
client_socket.close()
