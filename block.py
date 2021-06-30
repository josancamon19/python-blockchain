from cryptography.hazmat.primitives import hashes
import random


class DataClass:
    def __init__(self, string: str):
        self.string = string
    
    def __repr__(self):
        return self.string


class Block:
    
    def __init__(self, data, previous_block):
        """
        Block class, piece of a chain
        
        :param data: data to be encoded (Anything)
        :param previous_block:  Like a linked list (root Node, no parent -> None)
        """
        self.data = data
        self.previous_block: Block = previous_block
        self.previous_hash: bytes = previous_block.compute_hash() if previous_block else b''
        
        self.nonce = 0
        self.leading_zeros_nonce = 2
    
    def compute_hash(self):
        """
        Takes data + previous block hash, and generates this block hash
        :return: the hashed data + previous_hash
        """
        digest = hashes.Hash(hashes.SHA256())
        digest.update(bytes(str(self.data), 'utf-8'))
        digest.update(self.previous_hash)
        return digest.finalize()
    
    def is_valid(self):
        if not self.previous_block:
            return True
        return self.previous_block.compute_hash() == self.previous_hash
    
    def detect_tampering(self):
        """
        Detect tampering in the block chain from the block selected up to root
        """
        
        block = self
        while block:
            if not block.previous_block:
                print('Blockchain without tampering detected...')
                break
            
            if block.is_valid():
                block = block.previous_block
            else:
                print('Tampering detected on block',
                      block.previous_block.data, block.previous_block.compute_hash())
                break
    
    # -------- MINING PORTION -------------
    
    def compute_hash_with_nonce(self, nonce: str):
        """
        Takes data + previous block hash + a nonce, and generates a hash
        :param nonce: random str of any length
        :return: the hashed bytes
        """
        digest = hashes.Hash(hashes.SHA256())
        digest.update(bytes(str(self.data), 'utf-8'))
        digest.update(self.previous_hash)
        digest.update(bytes(nonce, 'utf-8'))
        return digest.finalize()
    
    def validate_nonce(self):
        return self.compute_hash_with_nonce(self.nonce)[:self.leading_zeros_nonce] \
               == bytes('\x00' * self.leading_zeros_nonce, 'utf-8')
    
    def find_nonce(self):
        """
        Alternative name: mine_block(self):
        - Generates nonces and the hash with that nonce
        - Then, if the hash first 2 characters contain n number of zeros (\x00) on the first 2 characters  (Nonce found)
        - Difficulty increases with the # of self.leading_zeros_nonce
        :return:
        """
        nonces_attempted = {}
        while True:
            nonce = self.generate_nonce()
            if nonces_attempted.get(nonce):
                continue
            
            new_hash = self.compute_hash_with_nonce(nonce)
            if new_hash[:self.leading_zeros_nonce] == b'\x00' * self.leading_zeros_nonce:  # contains 0
                print('Nonce is', nonce, 'Hash ->', new_hash)
                break
            
            nonces_attempted[nonce] = new_hash
            print(nonce, '...', new_hash[:self.leading_zeros_nonce])
        
        self.nonce = nonce
    
    def generate_nonce(self):
        """
        Generate a random nonce (within all ascii chars) of an arbitrary length
        :return: the nonce
        """
        return ''.join([chr(random.randint(0, 255)) for i in range(5 * self.leading_zeros_nonce)])


if __name__ == '__main__':
    block0 = Block('000', None)
    block1 = Block(111, block0)
    block2 = Block(DataClass('222'), block1)
    block3 = Block('333', block2)
    
    block3.detect_tampering()
