from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


def generate_keys():
    """
    Generate private and public keys
    :return: keys
    """
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = private.public_key()
    return private, public


def sign(message: str, private):
    """
    :param message: str message
    :param private: private key
    :return:
    """
    signature = private.sign(
        bytes(str(message), 'utf-8'),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    return signature


def verify(message: str, signature: str, public) -> bool:
    """
    A private key can be used to sign a message.
    This allows anyone with the public key to verify that the message was
    created by someone who possesses the corresponding private key.
    
    :param message: bytes str message
    :param signature: signed_message
    :param public: public key
    :return: boolean
    """
    try:
        public.verify(
            signature,
            bytes(str(message), 'utf-8'),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    except Exception as e:
        return False


if __name__ == '__main__':
    message = 'Message'
    
    private, public = generate_keys()
    signature = sign(message, private)
    result = verify(message, signature, public)
    print(result)
