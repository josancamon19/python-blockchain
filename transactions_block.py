from block import Block
from transaction import Transaction, get_4_key_pairs

miner_block_reward = 25


class TransactionsBlock(Block):
    def __init__(self, previous_block):
        super().__init__([], previous_block)
        
        self.total_transactions_input = 0
        self.total_transactions_output = 0
    
    def add_transaction(self, transaction):
        """
        Block data is a list of transactions in this case, remember in our Block, data can be anything
        :param transaction: Transaction object
        """
        
        self.data.append(transaction)
        self.__set_block_totals(transaction)
    
    def __set_block_totals(self, transaction):
        self.total_transactions_input += transaction.get_total_input()
        self.total_transactions_output += transaction.get_total_output()
    
    def is_valid(self):
        """
        - Block is_valid operation
        - Transaction is_valid_operation
        - Transactions total output equals or less than input+reward
        :return: boolean depending on 2 conditions mentioned above
        """
        if not super(TransactionsBlock, self).is_valid():
            return False
        
        for t in self.data:
            if not t.is_valid():
                return False
        
        # validate it does not contain more than the reward
        if not self.total_transactions_output <= (self.total_transactions_input + miner_block_reward):
            return False
        
        return True


def get_new_transaction() -> Transaction:
    """
    :return: Simple default transaction object
    """
    transaction = Transaction()
    transaction.add_input(public1, 1)
    transaction.add_output(public2, 1)
    transaction.sign(private1)
    return transaction


def get_reward_transaction() -> Transaction:
    """
    :return: Simple transaction object with a fee for the miner of .1
    """
    transaction = Transaction()
    transaction.add_input(public1, 1.1)
    transaction.add_output(public2, 1)
    transaction.sign(private1)
    return transaction


def get_miner_transaction(transactions_fees_to_collect: float = 0.0) -> Transaction:
    """
    :return: Simple miner transaction object
    """
    transaction = Transaction()
    transaction.add_output(public4, 25 + transactions_fees_to_collect)
    return transaction


if __name__ == '__main__':
    private1, public1, private2, public2, private3, public3, private4, public4 = get_4_key_pairs()
    
    genesis = TransactionsBlock(None)
    genesis.add_transaction(get_new_transaction())
    
    block1 = TransactionsBlock(genesis)
    block1.add_transaction(get_new_transaction())
    block1.add_transaction(get_new_transaction())
    
    block2 = TransactionsBlock(block1)
    block2.add_transaction(get_new_transaction())
    
    block3 = TransactionsBlock(block2)
    block3.add_transaction(get_new_transaction())
    block3.add_transaction(get_reward_transaction())
    block3.add_transaction(get_reward_transaction())
    block3.add_transaction(get_miner_transaction(.2))
    
    print(block3.is_valid())
    
    # block3.detect_tampering()
