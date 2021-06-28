from cryptography.hazmat.primitives import hashes


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


if __name__ == '__main__':
    block0 = Block('000', None)
    block1 = Block(111, block0)
    block2 = Block(DataClass('222'), block1)
    block3 = Block('333', block2)
    
    block3.detect_tampering()
