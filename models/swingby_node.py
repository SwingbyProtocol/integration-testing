"""
Module used to describe a SwingbyNode object
"""

import subprocess
import requests
import json
import os
import signal
import atexit
import time
import utils
import optparse

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SwingbyNode:
    """
    Enum used to index the location of each value in a raw array
    """
    METHOD = 1
    CURRENCY = 2
    ADDRESS = 4

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

    def wait_for_startup(self):
        if not utils.wait_until(self.is_running, timeout=60, label="Waiting for node startup"):
            raise Exception("Failed to wait for node startup. {}".format(self))

    def get_tss_address(self, symbol):
        sym = symbol.upper()
        if not self.tssAddresses[sym]:
            raise Exception("No tss address for symbol " + sym)
        return self.tssAddresses[sym]

    def calculate_swap(self, amount, from_ccy, to_ccy, address_to):
        ## calculate swap to get proof of work nonce
        res_calc = self.request("api/v1/swaps/calculate", {
            "amount": str(amount),
            "currency_from": from_ccy,
            "currency_to": to_ccy,
            "address_to": address_to
        })
        if res_calc['code'] != 200:
            raise Exception("Http code {} - ".format(res_calc['content']['message']))
        return res_calc['content']

    def create_swap(self, amount, from_ccy, to_ccy, address_to):
        now = time.time()
        ## calculate swap to get proof of work nonce
        res_calc = self.calculate_swap(amount, from_ccy, to_ccy, address_to)
        ## create swap using nonce
        print ("***", time.time() - now)
        res_swap = self.request("api/v1/swaps/create", {
            "amount": res_calc['send_amount'],
            "currency_from": from_ccy,
            "currency_to": to_ccy,
            "address_to": address_to,
            "nonce": res_calc['nonce']
        })
        print ("***", time.time() - now)
        if res_swap['code'] != 200:
            raise Exception("Http code {} - ".format(res_swap['content']['message']))
        res = res_swap['content']
        res['calc'] = res_calc
        return res

    def is_running(self):
        if self.proc == None:
            return False
        # check we get a response from the api
        status = self.fetch_status()
        if status != None:
            return True
        if status.code > 200 and status.code < 299:
            return True
        return False

    def fetch_status(self):
        status = self.request("api/v1/status")
        if status['code'] > 200 and status['code'] < 299:
            raise Exception("Got error code", status['code'])
        return status['content']

    def fetch_peers(self):
        peers = self.request("api/v1/peers")
        if peers['code'] > 200 and peers['code'] < 299:
            raise Exception("Got error code", peers['code'])
        return peers['content']

    def request(self, path, data=None):
        # if no data provided then request is GET otherwise POST
        endpoint = "{}:{}/{}".format(self.host, self.api_port, path)
        if data:
            print ("POST:", endpoint, "-", data)
            resp = requests.post(endpoint, verify=False, json=data, stream=True, timeout=15)
            print ("RECV:", resp.json())
        else:
            print ("GET:", endpoint)
            resp = requests.get(endpoint, stream=True, timeout=15)
            print ("RECV:", resp.json())
        return { 'code': resp.status_code, 'content': json.loads(resp.content) }

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
