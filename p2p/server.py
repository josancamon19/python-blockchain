import socket
import pickle
from transactions_block import TransactionsBlock

IP_ADDRESS = 'localhost'
TCP_PORT = 5005


def create_connection(ip_address: str = IP_ADDRESS):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip_address, TCP_PORT))
    s.listen()
    return s


def receive_block(connection) -> TransactionsBlock:
    new_socket, address = connection.accept()
    data = b''
    while True:
        packet = new_socket.recv(4096)
        if not packet:
            break
        data += packet
    return pickle.loads(data)


if __name__ == '__main__':
    connection = create_connection()
    block_received = receive_block(connection)
    while block_received:
        print('Block', block_received)
        block_received = receive_block(connection)
