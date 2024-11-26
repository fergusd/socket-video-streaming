import socket
import cv2
import pickle
import struct
import argparse
from config import SERVER_HOST, SERVER_PORT


def receive_video(displayEnabled):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_address = (SERVER_HOST, SERVER_PORT)
    print(f"Host IP: {SERVER_HOST}")

    # Bind the socket to the address and port
    server_socket.bind(socket_address)
    print("Socket bind complete")

    # Listen for incoming connections
    server_socket.listen(5)
    print("Socket now listening")

    while True:
        # Wait for a connection
        client_socket, addr = server_socket.accept()
        print("Connection from:", addr)

        if client_socket:
            # Initialize buffer for incoming data
            data = b""

            # Size of the packed frame length
            payload_size = struct.calcsize("Q")

            try:
                while True:
                    # Receive frame size
                    while len(data) < payload_size:
                        # Receive data in chunks
                        packet = client_socket.recv(4 * 1024)

                        # Exit if no data received
                        if not packet:
                            return
                
                        data += packet
            
                    # Unpack frame size
                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("Q", packed_msg_size)[0]

                    # Receive frame data based on the unpacked frame size
                    while len(data) < msg_size:
                        data += client_socket.recv(4 * 1024)
            
                    # Deserialize frame data
                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    frame = pickle.loads(frame_data)

                    # Display the frame
                    if(displayEnabled):
                        cv2.imshow("receiving...", frame)
                        key = cv2.waitKey(10)

            finally:
                client_socket.close()
                cv2.destroyAllWindows()

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--display', default=False, action='store_true')
    args = parser.parse_args()

    # Start streaming video
    stream_video(args.video)


if __name__ == "__main__":
    main()
