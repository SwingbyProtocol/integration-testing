"""
Module used as a interfeace to describe a generick websocket client
"""

import asyncio
import utils
import websockets
import socket
import json
import time
from threading import Thread

from pyee import EventEmitter

# websocket exceptions
from websockets.exceptions import ConnectionClosed

class Socket():
    def __init__(self, sId):
        self.ws = None
        self.isConnected = False
        self.id = sId

    def set_connected(self):
        self.isConnected = True

    def set_disconnected(self):
        self.isConnected = False

    def set_websocket(self, ws):
        self.ws = ws

def _start_event_worker():
    async def event_sleep_process():
        """
        sleeping process for event emitter to schedule on
        """
        while True:
            await asyncio.sleep(0)
    def start_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(event_sleep_process())
    event_loop = asyncio.new_event_loop()
    worker = Thread(target=start_loop, args=(event_loop,))
    worker.start()
    ee = EventEmitter(scheduler=asyncio.ensure_future, loop=event_loop)
    return ee

class GenericWebsocket:
    """
    Websocket object used to contain the base functionality of a websocket.
    Inlcudes an event emitter and a standard websocket client.
    """

    def __init__(self, host, max_retries=5, create_event_emitter=None):
        self.host = host
        self.ws = None
        self.max_retries = max_retries
        self.attempt_retry = True
        self.sockets = {}
        create_ee = create_event_emitter or _start_event_worker
        self.events = create_ee()
    
    def close(self):
        """
        Close all websocket connections
        """
        for s in self.sockets:
            s.ws.close()
            s.set_disconnected()

    def run(self):
        """
        Starte the websocket connection. This functions spawns the initial socket
        thread and connection.
        """
        self._start_new_socket()

    def get_task_executable(self):
        """
        Get the run indefinitely asyncio task
        """
        return self._run_socket()

    def _start_new_socket(self, socketId=None):
        if not socketId:
            socketId = len(self.sockets)
        def start_loop(loop):
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._run_socket())
        worker_loop = asyncio.new_event_loop()
        worker = Thread(target=start_loop, args=(worker_loop,))
        worker.start()
        return socketId

    def _wait_for_socket(self, socket_id):
        """
        Block until the given socket connection is open
        """
        def check_socket():
            socket = self.sockets.get(socket_id, False)
            if socket:
                if socket.isConnected and socket.ws:
                    return True
        if not utils.wait_until(check_socket, timeout=10, label="Waiting for indexer to connect"):
            raise Exception("Failed to connect to indexer")

    async def _connect(self, socket):
        async with websockets.connect(self.host) as websocket:
            self.sockets[socket.id].set_websocket(websocket)
            self.sockets[socket.id].set_connected()
            print("Wesocket connected to {}".format(self.host))
            while True:
                await asyncio.sleep(0)
                message = await websocket.recv()
                await self.on_message(socket.id, message)

    def get_socket(self, socketId):
        return self.sockets[socketId]

    async def _run_socket(self):
        retries = 0
        sId =  len(self.sockets)
        s = Socket(sId)
        self.sockets[sId] = s
        while retries < self.max_retries and self.attempt_retry:
            try:
                await self._connect(s)
                retries = 0
            except (ConnectionClosed, socket.error) as e:
                self.sockets[sId].set_disconnected()
                self._emit('disconnected')
                if (not self.attempt_retry):
                    return
                print(str(e))
                retries += 1
                # wait 5 seconds befor retrying
                print.info("Waiting 5 seconds before retrying...")
                await asyncio.sleep(5)
                print.info("Reconnect attempt {}/{}".format(retries, self.max_retries))
        print.info("Unable to connect to websocket.")
        self._emit('stopped')

    def remove_all_listeners(self, event):
        """
        Remove all listeners from event emitter
        """
        self.events.remove_all_listeners(event)

    def on(self, event, func=None):
        """
        Add a new event to the event emitter
        """
        if not func:
            return self.events.on(event)
        self.events.on(event, func)

    def once(self, event, func=None):
        """
        Add a new event to only fire once to the event
        emitter
        """
        if not func:
            return self.events.once(event)
        self.events.once(event, func)

    def _emit(self, event, *args, **kwargs):
        self.events.emit(event, *args, **kwargs)

    async def on_error(self, error):
        """
        On websocket error print and fire event
        """
        print(error)

    async def on_close(self):
        """
        On websocket close print and fire event. This is used by the data server.
        """
        print("Websocket closed.")
        self.attempt_retry = False
        for key, socket in self.sockets.items():
            await socket.ws.close()
        self._emit('done')

    async def on_open(self):
        """
        On websocket open
        """
        pass

    async def on_message(self, message):
        """
        On websocket message
        """
        pass
