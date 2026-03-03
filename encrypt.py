import os
from crypto_utils import encrypt_file


if __name__ == "__main__":

    encrypt_file("docs/text.txt", "docs/text.enc")
