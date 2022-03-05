import logging
import random
import bitsv

from pycoin.serialize import b2h

from cert_issuer.blockchain_handlers.bsv import tx_utils
from cert_issuer.config import ESTIMATE_NUM_INPUTS, V2_NUM_OUTPUTS
from cert_issuer.errors import InsufficientFundsError, Error
from cert_issuer.models import TransactionCreator, TransactionHandler
from cert_issuer.signer import FinalizableSigner


class TransactionV2Creator(TransactionCreator):
    def estimate_cost_for_certificate_batch(self, tx_cost_constants, num_inputs=ESTIMATE_NUM_INPUTS):
        total = tx_utils.calculate_tx_fee(tx_cost_constants, num_inputs, V2_NUM_OUTPUTS)
        return total

    def create_transaction(self, tx_cost_constants, issuing_address, inputs, op_return_value):
        fee = tx_utils.calculate_tx_fee(tx_cost_constants, len(inputs), V2_NUM_OUTPUTS)
        transaction = tx_utils.create_trx(
            op_return_value,
            fee,
            issuing_address,
            [],
            inputs)

        return transaction


class BitcoinTransactionHandler(TransactionHandler):
    def __init__(self, connector, tx_cost_constants, secret_manager, issuing_address, prepared_inputs=None,
                 transaction_creator=TransactionV2Creator()):
        self.connector = connector
        self.tx_cost_constants = tx_cost_constants
        self.secret_manager = secret_manager
        self.issuing_address = issuing_address
        self.prepared_inputs = prepared_inputs
        self.transaction_creator = transaction_creator

    def ensure_balance(self):
        # ensure the issuing address has sufficient balance
        balance = self.connector.get_balance(self.issuing_address, self.secret_manager)

        transaction_cost = self.transaction_creator.estimate_cost_for_certificate_batch(self.tx_cost_constants)
        logging.info('%s address balance is %d satoshis', self.issuing_address, balance)
        logging.info('Total cost estimate will be %d satoshis', transaction_cost)

        if transaction_cost > balance:
            error_message = 'Please add {} satoshis to the address {}'.format(
                transaction_cost - balance, self.issuing_address)
            logging.error(error_message)
            raise InsufficientFundsError(error_message)

    def issue_transaction(self, blockchain_bytes):
        txid = self.connector.broadcast_op_return(blockchain_bytes, self.secret_manager)
        return txid
