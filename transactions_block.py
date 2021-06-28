from block import Block
from transaction import Transaction, get_4_key_pairs


class TransactionsBlock(Block):
    def __init__(self, previous_block):
        super().__init__([], previous_block)
    
    def add_transaction(self, transaction):
        self.data.append(transaction)
    
    def is_valid(self):
        if not super(TransactionsBlock, self).is_valid():
            return False
        
        for t in self.data:
            if not t.is_valid():
                return False
        
        return True


def get_new_transaction() -> Transaction:
    transaction = Transaction()
    transaction.add_input(public1, 1)
    transaction.add_output(public2, 1)
    transaction.sign(private1)
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
    
    block2.is_valid()
