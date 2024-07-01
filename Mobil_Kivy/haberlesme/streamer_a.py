import cv2
import socket
import pickle
import struct

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)

# Initialize socket connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5000))
server_socket.listen(5)

# Accept client connection
client_socket, addr = server_socket.accept()

while True:
    # Read frame from camera
    ret, frame = cap.read()

    # Serialize frame
    data = pickle.dumps(frame)
    message_size = struct.pack("L", len(data))

    # Send frame size
    client_socket.sendall(message_size + data)

# Release resources
cap.release()
server_socket.close()
