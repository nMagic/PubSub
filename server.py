#!/usr/bin/env python3
# coding: utf-8

import zmq
import asyncio
import zmq.asyncio
from db import Publication
import peewee
from config import *


class Server:
    def __init__(self, port: str):
        self.ctx = zmq.asyncio.Context()
        self.socket_sub_pub = self.ctx.socket(zmq.PUB)
        self.socket_sub_pub.bind("tcp://*:%s" % port)
        self.socket_server_client = self.ctx.socket(zmq.REP)
        self.socket_server_client.bind("tcp://*:%s" % str(int(port) + 1))
        try:
            Publication.create_table()  # Try to create publication table in db
        except peewee.OperationalError:
            pass

    def __del__(self):
        self.socket_server_client.close()
        self.socket_sub_pub.close()

    @staticmethod
    def publication_posted(publication: Publication):
        publication.it_posted = True
        publication.save()
        print("Publication %s tagged like posted..." % publication.content)

    async def post_publication(self, publication: Publication):
        await self.socket_sub_pub.send_string("%s %s" % (publication.title, publication.content), )
        print("Publication %s sended..." % publication.content)
        self.publication_posted(publication)

    async def check_db(self):
        """
        Check unposted publications in database.

        :return:
        """
        while True:
            need_to_post = Publication.select().where(Publication.it_posted == 0)
            if len(need_to_post) > 0:
                for publication in need_to_post:
                    await self.post_publication(publication)
            await asyncio.sleep(0)

    @staticmethod
    def add_publication_in_db(publication: Publication):
        publication.save()
        print("Publication %s added in db..." % publication.content)

    async def wait_new_publication(self):
        """
        Wait for new publications, that will be added to the database.

        :return:
        """
        while True:
            publication = await self.socket_server_client.recv_string()
            await self.socket_server_client.send_string("OK")
            title, content = publication.split(' ')[0], ' '.join(publication.split(' ')[1:])
            self.add_publication_in_db(Publication(title=title, content=content))

    def start(self):
        ioloop = asyncio.get_event_loop()
        ioloop.create_task(self.check_db())
        ioloop.create_task(self.wait_new_publication())
        ioloop.run_forever()



if __name__ == "__main__":
    server = Server(PORT)
    server.start()
