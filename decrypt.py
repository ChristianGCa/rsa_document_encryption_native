import json
from crypto_utils import decrypt_file

if __name__ == "__main__":

    with open("keys/private_key.json", "r") as f:
        private_key = json.load(f)
    keys = tuple(private_key.values())
    print(keys)
    decrypt_file(
        "docs/text.enc",
        "docs/text_decrypted.txt",
        keys,
    )