#!/usr/bin/env python3
# coding: utf-8

import zmq
from config import *


class Publisher:
    def __init__(self, port):
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:%s" % str(int(port) + 1))

    def __del__(self):
        self.socket.close()

    def send_publication(self, publication: str):
        self.socket.send_string(publication)
        self.socket.recv_string()


if __name__ == "__main__":
    name = input("Name: ")
    publisher = Publisher(PORT)
    while True:
        publication = input("Publication: ")
        print("%s %s" % (name, publication))
        publisher.send_publication("%s %s" % (name, publication))
