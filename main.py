import os
import json
from crypto_utils import encrypt_file, decrypt_file

def run_demo():

    original_file = "docs/text.txt"
    encrypted_file = "docs/text.enc"
    restored_file = "docs/final_text.txt"
    public_key_file = "keys/public_key.json"
    private_key_file = "keys/private_key.json"

    encrypt_file(original_file, encrypted_file)

    # pegar a chaves do arquivo

    with open(private_key_file, "r") as f:
        private_key = json.load(f)

    decrypt_file(encrypted_file, restored_file, private_key)

    with open(restored_file, "r", encoding="utf-8") as f:
        resultado = f.read()
        print("\nConteúdo restaurado:")
        print(resultado)


if __name__ == "__main__":
    run_demo()