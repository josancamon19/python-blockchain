from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import signatures


class NegativeAmountException(Exception):
    pass


class Transaction:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.signatures = []
        self.required_signatures = []
        
        self.transaction_fee = 0
    
    def add_input(self, public_address, amount):
        """
        Take certain amount from a public address
        :param public_address: Public address
        :param amount: # coins
        """
        if amount < 0:
            raise NegativeAmountException()
        
        self.inputs.append((public_address, amount))
        
        # Inputs are always required to sign
        self.add_required(public_address)
        self.find_transaction_fee()
    
    def add_output(self, public_address, amount):
        """
        Send certain amount of coins to a public address
        :param public_address: Public address
        :param amount: coins
        """
        if amount < 0:
            raise NegativeAmountException()
        
        self.outputs.append((public_address, amount))
        self.find_transaction_fee()
    
    def get_total_input(self):
        return sum([amount for _, amount in self.inputs])
    
    def get_total_output(self):
        return sum([amount for _, amount in self.outputs])
    
    def find_transaction_fee(self):
        self.transaction_fee = self.get_total_input() - self.get_total_output()
    
    def add_required(self, public_address):
        """
        Add public address as a required signature
        :param public_address: Public address
        """
        self.required_signatures.append(public_address)
    
    def sign(self, private):
        """
        With a private key, sign the transaction, and save the signature
        :param private: Private key
        """
        signature = signatures.sign(self.__gather(), private)
        self.signatures.append(signature)
    
    def is_valid(self):
        """
        - Length signatures == length required signatures
        - verify signature of each party involved in the operation
        :return:
        """
        if len(self.signatures) != len(self.required_signatures):
            print('Not signed by all required parties')
            return False
        
        for i, required in enumerate(self.required_signatures):
            if not signatures.verify(self.__gather(), self.signatures[i], required):
                print('Invalid signature verification')
                return False
        
        return True
    
    def __gather(self):
        """
        Transaction data to be signed
        :return: the transaction data representation
        """
        return [self.inputs, self.outputs, self.required_signatures]
    
    def setup_for_pickle(self):
        for i, public_key in enumerate(self.inputs):
            self.inputs[i] = self.get_key_public_bytes(public_key[0]), public_key[1]
        
        for i, public_key in enumerate(self.outputs):
            self.outputs[i] = self.get_key_public_bytes(public_key[0]), public_key[1]
        
        for i, public_key in enumerate(self.required_signatures):
            self.required_signatures[i] = self.get_key_public_bytes(public_key)
    
    def load_from_pickle(self):
        for i, public_key in enumerate(self.inputs):
            self.inputs[i] = self.get_key_from_public_bytes(public_key[0]), public_key[1]
        
        for i, public_key in enumerate(self.outputs):
            self.outputs[i] = self.get_key_from_public_bytes(public_key[0]), public_key[1]
        
        for i, public_key in enumerate(self.required_signatures):
            self.required_signatures[i] = self.get_key_from_public_bytes(public_key)
            
        print(self.__gather())
    
    @staticmethod
    def get_key_public_bytes(key):
        return key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    @staticmethod
    def get_key_from_public_bytes(pem_bytes: bytes):
        return serialization.load_pem_public_key(pem_bytes, backend=default_backend())


def get_4_key_pairs():
    """
    Generate 4 different public/private key pairs for testing
    :return: 4 key pairs
    """
    private1, public1 = signatures.generate_keys()
    private2, public2 = signatures.generate_keys()
    private3, public3 = signatures.generate_keys()
    private4, public4 = signatures.generate_keys()
    
    return private1, public1, private2, public2, private3, public3, private4, public4


def get_transaction1():
    """
    Simple transaction
    """
    private1, public1, private2, public2, private3, public3, private4, public4 = get_4_key_pairs()
    
    transaction = Transaction()
    
    transaction.add_input(public1, 1)
    transaction.add_output(public2, 1)
    
    transaction.sign(private1)
    
    return transaction


def get_transaction2():
    """
    Simple 1 input, 2 outputs transaction
    """
    private1, public1, private2, public2, private3, public3, private4, public4 = get_4_key_pairs()
    transaction = Transaction()
    transaction.add_input(public1, 2)
    transaction.add_output(public2, 1)
    transaction.add_output(public3, 1)
    transaction.sign(private1)
    return transaction


def get_transaction3():
    """
    Testing Escrow simple transaction
    """
    private1, public1, private2, public2, private3, public3, private4, public4 = get_4_key_pairs()
    transaction = Transaction()
    transaction.add_input(public1, 1.2)
    transaction.add_output(public2, 1.1)
    
    transaction.add_required(public3)  # arbiter
    transaction.sign(private1)
    transaction.sign(private3)
    
    return transaction


def get_transaction4():
    """
    Invalid transaction, required public1, signed with private2
     (user receiving coins, trying to use an invalid key)
    """
    private1, public1, private2, public2, private3, public3, private4, public4 = get_4_key_pairs()
    transaction = Transaction()
    transaction.add_input(public1, 1)
    transaction.add_output(public2, 1)
    transaction.sign(private2)
    return transaction


def get_transaction5():
    """
    Invalid transaction, Escrow transaction, not signed by arbiter
    """
    private1, public1, private2, public2, private3, public3, private4, public4 = get_4_key_pairs()
    transaction = Transaction()
    transaction.add_input(public1, 1.2)
    transaction.add_output(public2, 1.1)
    
    transaction.add_required(public3)  # arbiter
    transaction.sign(private1)
    # arbiter sign missing here
    
    return transaction


def get_transaction6():
    """
    Invalid transaction, input < output
    """
    private1, public1, private2, public2, private3, public3, private4, public4 = get_4_key_pairs()
    transaction = Transaction()
    transaction.add_input(public1, 1)
    transaction.add_output(public2, 2)
    transaction.sign(private1)
    return transaction


def get_transaction7():
    """
    Invalid transaction, input negative
    """
    private1, public1, private2, public2, private3, public3, private4, public4 = get_4_key_pairs()
    transaction = Transaction()
    try:
        transaction.add_input(public1, -1)
        transaction.add_output(public2, -1)
    except NegativeAmountException:
        print('Transaction 7 negative amounts exception ...\n')
        return
    
    transaction.sign(private1)
    return transaction


def get_new_transaction() -> Transaction:
    """
    :return: Simple default transaction object
    """
    private1, public1, private2, public2, private3, public3, private4, public4 = get_4_key_pairs()
    transaction = Transaction()
    transaction.add_input(public1, 1)
    transaction.add_output(public2, 1)
    transaction.sign(private1)
    return transaction


def get_reward_transaction() -> Transaction:
    """
    :return: Simple transaction object with a fee for the miner of .1
    """
    private1, public1, private2, public2, private3, public3, private4, public4 = get_4_key_pairs()
    transaction = Transaction()
    transaction.add_input(public1, 1.1)
    transaction.add_output(public2, 1)
    transaction.sign(private1)
    return transaction


def get_miner_transaction(transactions_fees_to_collect: float = 0.0) -> Transaction:
    """
    :return: Simple miner transaction object
    """
    private1, public1, private2, public2, private3, public3, private4, public4 = get_4_key_pairs()
    transaction = Transaction()
    transaction.add_output(public4, 25 + transactions_fees_to_collect)
    return transaction


if __name__ == '__main__':
    
    transactions = [get_transaction1(), get_transaction2(), get_transaction3(), get_transaction4(), get_transaction5(),
                    get_transaction6(), get_transaction7()]
    
    for i, t in enumerate(transactions):
        if not t:
            continue
        if t.is_valid():
            print(i + 1, 'Success! transaction is valid\n')
        else:
            print(i + 1, 'ERROR! Invalid transaction\n')
