"""
Module used to describe a SwingbyNode object
"""

import subprocess
import json
import os
import signal
import atexit
import time
import utils
import optparse

from swingby import NodeHttpClient

def _exec_node(executable, *args):
    return subprocess.Popen([executable] + list(args), stdout=subprocess.PIPE)

class SwingbyNode:
    """
    Some info on the node
    """

    def __init__(self, node_id, node_home, node_exec, host="http://127.0.0.1", flags=""):
        self.node_id = node_id
        self.peer_port = 12121
        self.api_port = 8067
        self.preset = 1
        self.node_home = node_home
        self.proc = None
        self.node_exec = node_exec
        self.host = host
        self.flags = []
        self.tssAddresses = {
            "BTC": "mz3emZezkCbXYN967smwgt2oxkqs9qe1Xg",
            "BTC.B": "tbnb1edqgw7nvldgfx5sqq4n3l96xxrj0h04satqyaa",
            "BTC.B-918": "tbnb1edqgw7nvldgfx5sqq4n3l96xxrj0h04satqyaa",
            "BNB": "tbnb1edqgw7nvldgfx5sqq4n3l96xxrj0h04satqyaa"
        }
        flags = flags.split()
        for f in flags:
            if "preset" in f:
                self.preset = int(f.split('=')[1])
                continue
            if "p2p.port" in f:
                self.peer_port = int(f.split('=')[1])
            if "rest.port" in f:
                self.api_port = int(f.split('=')[1])
            self.flags += [f]
        self.flags += ['--home={}'.format(self.node_home)]
        self.sdk = NodeHttpClient("{}:{}".format(self.host, self.api_port))

    def wait_for_startup(self):
        if not utils.wait_until(self.is_running, timeout=60, label="Waiting for node startup"):
            raise Exception("Failed to wait for node startup. {}".format(self))

    def get_tss_address(self, symbol):
        addresses = self.sdk.get_tss_addresses()
        sym = symbol.upper()
        for addr in addresses:
            if addr['currency'].upper() == sym:
                return addr['address']
        raise Exception("No tss address for symbol " + sym)

    def create_swap(self, amount, from_ccy, to_ccy, address_to):
        # address_to, amount, currency_from, currency_to,
        return self.sdk.swap(address_to, amount, from_ccy, to_ccy)

    def is_running(self):
        if self.proc == None:
            return False
        try:
            status = self.sdk.get_status()
            if status:
                return True
        except Exception:
            return False
        return False

    def fetch_status(self):
        return self.sdk.get_status()

    def fetch_peers(self):
        return self.sdk.get_peers()

    def start(self):
        print ("Starting {} with flags {}".format(self, self.flags))
        self.proc = _exec_node(self.node_exec, *self.flags)
        self.wait_for_startup()
        atexit.register(self.stop)

    def stop(self):
        print ("Stopping {}".format(self))
        if self.proc != None:
            self.proc.kill()
            self.proc.wait()
            self.proc = None

    def __str__(self):
        ''' Allow us to print the SwingbyNode object in a pretty format '''
        text = "SwingbyNode <{} pid={} home={} api_host={}:{} peer_host={}:{}>"
        pid = None
        if self.proc:
            pid = self.proc.pid
        return text.format(self.node_id, pid, self.node_home, self.host, self.api_port, self.host, self.peer_port)

testnet_node = SwingbyNode("", "", "", host="https://testnet-node.swingby.network", flags="--rest.port=443")
# testnet_node = SwingbyNode("", "", "", host="http://localhost", flags="--rest.port=8067")
