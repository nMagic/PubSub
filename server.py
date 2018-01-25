#!/usr/bin/env python3
# coding: utf-8

import zmq
import asyncio
import zmq.asyncio
from db import Publication
import peewee


class Server:
    def __init__(self, port: str):
        self.ctx = zmq.asyncio.Context.instance()
        self.socket_sub_pub = self.ctx.socket(zmq.PUB)
        self.socket_sub_pub.bind("tcp://*:%s" % port)
        self.socket_server_client = self.ctx.socket(zmq.REP)
        self.socket_server_client.bind("tcp://*:%s" % str(int(port) + 1))

    def __del__(self):
        print(self.socket_server_client.close())
        print(self.socket_sub_pub.close())

    def check_db(self):
        """
        Check unposted publications in database.

        :return:
        """
        try:
            Publication.create_table()  # Try to create publication table in db
        except peewee.IntegrityError:
            pass
        need_to_post = [publication for publication in Publication.select().where(Publication.it_posted == False)]
        if len(need_to_post) > 0:
            pass  # TODO: Handle unposted publications.

    def start(self):
        self.check_db()


if __name__ == "__main__":
    pass
