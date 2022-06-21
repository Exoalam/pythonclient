import base64
import json
import socket
import threading
from io import BytesIO
import cv2
import PIL.Image
import numpy


def client_send():
    feed = cv2.VideoCapture(0)
    while True:
        s = socket.socket()
        port = 55667
        s.connect(('127.0.0.1', port))
        ret, frame = feed.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = PIL.Image.fromarray(frame)
        # with open("i.jpg", "rb") as image_file:
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        data = base64.b64encode(buffered.getvalue())
        outgoing_data = '''
        {
            "code":"IDLE",
            "data":"''' + data.decode("utf-8") + '''",
            "name":"Nafiul"
        }
        '''
        print(outgoing_data)
        s.send(outgoing_data.encode())
        cv2.waitKey(500)
        s.close()
        s = socket.socket()
        print("Server Created")
        port = 25432
        s.bind(('', port))
        print("socket binded to %s" % (port))
        s.listen()
        print("socket is listening")
        c, addr = s.accept()
        print('Got connection from', addr)
        incoming_data = c.recv(6553600).decode()
        json_file = json.loads(incoming_data)
        image = json_file['data']
        name = json_file['code']
        im = PIL.Image.open(BytesIO(base64.b64decode(image)))
        frame = cv2.cvtColor(numpy.array(im), cv2.COLOR_RGB2BGR)
        cv2.imshow('Video', frame)
        cv2.waitKey(1)
        s.close()
        c.close()


if __name__ == '__main__':
    client_send()





