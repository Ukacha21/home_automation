import cv2
import requests

"""
Ethernet
IPv4 Address. . . . . . . . . . . : 192.168.42.27

Wirels
IPv4 Address. . . . . . . . . . . :
"""

def main():
    url = 'http://192.168.42.27:8080/video_feed'  # Replace with your server's IP address and port

    stream = requests.get(url, stream=True)

    if stream.status_code == 200:
        bytes = stream.content
        while True:
            frame = bytes.find(b'\r\n\r\n')
            if frame != -1:
                frame_data = bytes[:frame]
                bytes = bytes[frame+4:]
                img = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow('Video Stream', img)
                if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
                    break
    else:
        print("Error: Could not connect to the server.")

if __name__ == "__main__":
    main()