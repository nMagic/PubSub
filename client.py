#!/usr/bin/env python3
# coding: utf-8

import zmq
from config import *


class Client:
    def __init__(self, port: str):
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:%s" % port)

    def __del__(self):
        self.socket.close()

    @staticmethod
    def print_publication(publication: str):
        print(publication)

    def check_publication(self):
        publication = self.socket.recv_string()
        self.print_publication(publication)

    def subscribe(self, topicname: str):
        self.socket.setsockopt_string(zmq.SUBSCRIBE, topicname)


if __name__ == "__main__":
    client = Client(PORT)
    topic = input("Enter the name of the topic for the subscription or leave it blank: ")
    if topic != '':
        client.subscribe(topic)
    while topic != '':
        topic = input("Enter the name of the topic for the subscription or leave it blank: ")
        if topic != '':
            client.subscribe(topic)
    while True:
        client.check_publication()

