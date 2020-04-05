"""
This module contains a group of different models which
are used to define data types
"""

from .swingby_node import SwingbyNode, testnet_node
from .btc_indexer_client import BtcIndexerClient
from .bnb_client import BnbClient, bnb_address
from .btc_client import BtcClient, btc_address
from .block_cypher import BlockCypherClient, block_cypher_client

NAME = 'models'
