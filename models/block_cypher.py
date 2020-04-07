"""
Module used to describe a BlockCypherClient object
"""
import json
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BlockCypherClient:

    responses = []

    def __init__(self, testnet=True):
        self.host = "https://api.blockcypher.com/v1/btc/main"
        if testnet:
            self.host = "https://api.blockcypher.com/v1/btc/test3"

    def get_latest_txs(self):
        endpoint = "{}/{}".format(self.host, "txs")
        res = self.request(endpoint)
        if res['code'] != 200:
            raise Exception("Http code {} - ".format(res['content']))
        return res['content']

    def get_latest_tx(self):
        txs = self.get_latest_txs()
        if len(txs) > 0:
            return txs[0]
        return None

    def get_height(self):
        endpoint = self.host
        res = self.request(endpoint)
        if res['code'] != 200:
            raise Exception("Http code {} - ".format(res['content']))
        return res['content']['height']

    def request(self, endpoint, data=None):
        # if no data provided then request is GET otherwise POST
        if data:
            print ("POST:", endpoint, "-", data)
            resp = requests.post(endpoint, verify=False, json=data, stream=True, timeout=15)
            print ("RECV:", resp.json())
        else:
            print ("GET:", endpoint)
            resp = requests.get(endpoint, stream=True, timeout=15)
            print ("RECV:", resp.json())
        return { 'code': resp.status_code, 'content': json.loads(resp.content) }

block_cypher_client = BlockCypherClient(testnet=True)
