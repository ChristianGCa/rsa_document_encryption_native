import os
import glob


def delete_files():
    paths = [
        "docs/*.enc",
        "docs/final_text.txt",
        "docs/text_decrypted.txt",
        "keys/public_key.json",
        "keys/private_key.json",
    ]

    for path in paths:
        # Se tiver wildcard (*), usa glob
        if "*" in path:
            for file in glob.glob(path):
                os.remove(file)
                print(f"Arquivo excluído: {file}")
        else:
            if os.path.exists(path):
                os.remove(path)
                print(f"Arquivo excluído: {path}")
            else:
                print(f"Arquivo não encontrado: {path}")


if __name__ == "__main__":
    delete_files()
