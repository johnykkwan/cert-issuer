"""
Connectors wrap the details of communicating with different Bitcoin clients and implementations.
"""
import io
import logging
import time
from abc import abstractmethod
import bitsv

import bitcoin.rpc
import requests
from bitcoin.core import CTransaction
from cert_core import Chain
from cert_issuer.errors import InsufficientFundsError, Error
from pycoin.serialize import b2h, b2h_rev, h2b, h2b_rev
from pycoin.services import providers
from pycoin.services.chain_so import ChainSoProvider
from pycoin.services.insight import InsightProvider
from pycoin.services.providers import service_provider_methods
from pycoin.tx.Spendable import Spendable

import cert_issuer.config
from cert_issuer import helpers
from cert_issuer.errors import BroadcastError

try:
    from urllib2 import urlopen, HTTPError
    from urllib import urlencode
except ImportError:
    from urllib.request import urlopen, HTTPError
    from urllib.parse import urlencode

BROADCAST_RETRY_INTERVAL = 30
MAX_BROADCAST_ATTEMPTS = 3


def to_hex(transaction):
    s = io.BytesIO()
    transaction.stream(s)
    tx_as_hex = b2h(s.getvalue())
    return tx_as_hex

class ServiceProviderConnector(object):
    @abstractmethod
    def get_balance(self, address):
        pass

    def broadcast_tx(self, tx):
        pass

class MockServiceProviderConnector(ServiceProviderConnector):
    def get_balance(self, address):
        pass

    def broadcast_tx(self, tx):
        pass


class BitcoinServiceProviderConnector(ServiceProviderConnector):
    def __init__(self, bitcoin_chain, bitcoind=False):
        self.bitcoin_chain = bitcoin_chain
        self.bitcoind = bitcoind
        self.network = 'main' if (bitcoin_chain == Chain.bsv_mainnet) else 'test'

    def spendables_for_address(self, bitcoin_address):
        return []

    def get_unspent_outputs(self, address):
        """
        Get unspent outputs at the address
        :param address:
        :return:
        """
        return None

    def get_balance(self, issuing_address, secret_manager):
        """
        Get balance available to spend at the address
        """
        secret_manager.start()
        key = bitsv.Key(secret_manager.wif, self.network)
        secret_manager.stop()
        balance = int(key.get_balance())
        address = key.address

        if address != issuing_address:
            error_message = 'Derived {} address is not the same as issuing {} address'.format(
                address, issuing_address)
            logging.error(error_message)
            raise Error(error_message)

        return balance

    def broadcast_op_return(self, blockchain_bytes, secret_manager):
        """
        Broadcast the transaction through the configured set of providers
        """
        secret_manager.start()
        key = bitsv.Key(secret_manager.wif, self.network)
        list_of_pushdata = ([blockchain_bytes])
        txid = key.send_op_return(list_of_pushdata)
        secret_manager.stop()

        return txid 

# configure api tokens
config = cert_issuer.config.CONFIG
blockcypher_token = None if config is None else config.blockcypher_api_token
