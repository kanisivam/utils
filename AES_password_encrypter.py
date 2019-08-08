import argparse
import traceback
import sys
from Crypto.Cipher import AES
import base64

MASTER_KEY = "Son-br-base-key-to-use-as-encyrption-key"


class AESCipher(object):
    """
    This class implements the AESCipher Encryption/Decryption for the given text.
    Encrypt the text with the given secret key and decrypt the encrypted text with the same secret key.
    """

    def encrypt(self, clear_text):
        """
        Encrypt the given clear text with the master key.
        :param clear_text: text to be encrypted
        :return: encrypted text
        """
        try:
            enc_secret = AES.new(MASTER_KEY[:32])
            tag_string = (str(clear_text) +
                      (AES.block_size -
                       len(str(clear_text)) % AES.block_size) * "\0")
            cipher_text = base64.b64encode(enc_secret.encrypt(tag_string))
            return cipher_text
        except Exception as e:
            print("Unable to Encrypt Given Text : {0} , Error {1}".format(clear_text,e))

    def decrypt(self,cipher_text):
        """
        Decrypp the Given clear text with the master key.
        :param cipher_text: text to be decrypted.
        :return:
        """
        try:
            dec_secret = AES.new(MASTER_KEY[:32])
            raw_decrypted = dec_secret.decrypt(base64.b64decode(cipher_text))
            clear_val = raw_decrypted.rstrip("\0")
            return clear_val
        except TypeError:
            print("Error in Decryption ,  Given Text is not Encrypted with the Expected Secret Key: {0}".format(cipher_text))
        except Exception as e:
            print("Error in Decryption for Text :{0} , {1}".format(cipher_text, e))


#######################################################


def check_arguments(args=None):
    """
    Parse the arguments  specified by user and parse it and return args and
    :param args: arguments from user
    :return:args
    """
    try:
        parser = argparse.ArgumentParser(description='PASSWORD ENCRYPTION')
        parser.add_argument('-p', '--password', required=True, nargs='+',
                            help='Specify One/More Password to Encrypt.  Usage: Pass1 Pass2')
        args = parser.parse_args()
    except Exception as e:
        print(traceback.format_exc())
        sys.stderr.write(repr(e) + "\n")
        sys.exit(-1)
    return args


def start_encryption(texts_to_encrypt):
    """
    Start the encrytion for the given plain texts
    :param passwords_to_encrypt:
    :return: encrypted texts
    """
    cipher = AESCipher()
    encrypted = []
    for plain_text in texts_to_encrypt:
        try:
            encrypted_text = cipher.encrypt(plain_text)
            encrypted.append(encrypted_text)
            print(plain_text, encrypted_text)
        except Exception as e:
            print("Unable to Encrypt the Given Text {0} : {1}".format(plain_text,e))
    return encrypted


def main():
    """
    Get plain texts to be encrypted . do AES encryption and returns
    the encrypted text
    :return:
    """
    try:
        args = check_arguments()
        texts_to_encrypt = args.password
        start_encryption(texts_to_encrypt)
    except Exception as e:
        print("Error in Encryption : {0}".format(e))

if False and __name__ == "__main__":
    main()





