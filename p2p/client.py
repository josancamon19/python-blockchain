import server
import socket
from transactions_block import TransactionsBlock
from transaction import get_new_transaction
import pickle


def init_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send_block(s, block: TransactionsBlock):
    s.connect((server.IP_ADDRESS, server.TCP_PORT))
    data = pickle.dumps(block)
    s.send(data)
    return False


if __name__ == '__main__':
    connection = init_socket()
    
    genesis = TransactionsBlock(None)
    t = get_new_transaction()
    t.setup_for_pickle()
    genesis.add_transaction(t)
    
    block1 = TransactionsBlock(genesis)
    t = get_new_transaction()
    t.setup_for_pickle()
    block1.add_transaction(t)
    
    send_block(connection, block=block1)
    
    block1.transactions_from_pickle()
    block1.is_valid()
