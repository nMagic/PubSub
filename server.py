#!/usr/bin/env python3
# coding: utf-8

import zmq
import asyncio
import zmq.asyncio


class Server:
    def __init__(self, port):
        self.ctx = zmq.asyncio.Context.instance()
        self.socket_sub_pub = self.ctx.socket(zmq.PUB)
        self.socket_sub_pub.bind("tcp://*:%s" % port)
        self.socket_server_client = self.ctx.socket(zmq.REP)
        self.socket_server_client.bind("tcp://*:%s" % str(int(port) + 1))

    def __del__(self):
        print(self.socket_server_client.close())
        print(self.socket_sub_pub.close())


if __name__ == "__main__":
    pass
