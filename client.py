import socket
import cv2
import pickle
import struct
import argparse
import time
from config import SERVER_HOST, SERVER_PORT


def send_video(video_path, displayEnabled):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Open the video file
    vid = cv2.VideoCapture(video_path)
    while vid.isOpened():
        time.sleep(0.1)
        success, frame = vid.read()

        if success:
            # Serialize the frame
            data = pickle.dumps(frame)

            # Pack the frame size and data
            message = struct.pack("Q", len(data)) + data

            # Send data to the client
            client_socket.sendall(message)

            # Display the frame being sent
            if(displayEnabled):
                cv2.imshow("sending...", frame)
                key = cv2.waitKey(10)
            else:
                print((time.time()*1000),"<Tx Frame>")

            # Release the video capture object
            vid.release()    

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, type=str)
    parser.add_argument('--display', default=False, action='store_true')
    args = parser.parse_args()
    send_video(args.video, args.display)

if __name__ == "__main__":
    main()
