"""Some examples of RSA to encrypt and decrypt files
"""

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


def gen_pub_private_keys(pub_key_file, pri_key_file):
    key = RSA.generate(2048)
    private_key = key.exportKey()
    print('writing to {}'.format(pri_key_file))
    file_out = open(pri_key_file, 'wb')
    file_out.write(private_key)

    print('writing to {}'.format(pub_key_file))
    public_key = key.publickey().exportKey()
    file_out = open(pub_key_file, 'wb')
    file_out.write(public_key)


def encrypt(pub_key_file, input_file, output_file):
    """Encrypts the AWS credentials into a file.

    Regenerate the encryped file if necessary, the data format is as below.
    ```
    public_key
    private_key
    ```
    """
    data = open(input_file).read().encode('utf-8')
    file_out = open(output_file, 'w')

    pub_key = RSA.import_key(open(pub_key_file).read())
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(pub_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]


def decrypt(private_key_file, input_file):
    """Decrypts the AWS credentials from a file."""
    file_in = open(input_file, 'r')

    private_key = RSA.import_key(open(private_key_file).read())
    enc_session_key, nonce, tag, ciphertext = [
        file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    return cipher_aes.decrypt_and_verify(ciphertext, tag).decode('utf-8')


def case_gen_keys():
    print('=== case_gen_keys ===')
    gen_pub_private_keys('rsa.pub', 'rsa')

def case_encrypt_and_decrypt():
    """Run command line below beforehand:
    ```
    $ echo -e "I met aliens. Here is the map to the UFO.\nLet us meet at Golden Gate Bridge north at 3:16pm Mar 2019" > data.raw
    ```
    """
    print('=== case_encrypt_and_decrypt ===')
    encrypt('rsa.pub', 'data.raw', 'data.encrypt')
    data = decrypt('rsa', 'data.encrypt')
    print(data)


case_gen_keys()
case_encrypt_and_decrypt()
