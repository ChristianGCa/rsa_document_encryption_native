import json
import os

from .math_operations import modular_inverter, generate_prime


BIT_LENGTH = 1024
BLOCK_SIZE = (BIT_LENGTH // 8) - 1
PUBLIC_KEY_PATH = "keys/public_key.json"
PRIVATE_KEY_PATH = "keys/private_key.json"


def encrypt_file(input_path, output_path=None):
    """Encrypt `input_path` to `output_path`.

    This function will always generate a new RSA keypair, save both public and
    private keys to `keys/public_key.json` and `keys/private_key.json`, and then
    use the generated public key to encrypt the file.

    If `output_path` is None, the output file will be `input_path + ".enc"`.
    """
    if output_path is None:
        output_path = input_path + ".enc"

    public_key, private_key = generate_keys()
    e, n = public_key
    d, _ = private_key
    save_keys(e, d, n)

    print(f"Criptografando: {input_path} -> {output_path}")

    with open(input_path, 'rb') as f_in, open(output_path, 'w') as f_out:
        while True:
            chunk = f_in.read(BLOCK_SIZE)
            if not chunk:
                break

            chunk_len = len(chunk)
            m = int.from_bytes(chunk, byteorder='big')
            c = pow(m, e, n)

            # Save the original chunk length so we can restore leading zeros.
            f_out.write(f"{chunk_len}:{c}\n")


def decrypt_file(input_path, output_path, private_key):
    # Accept either a dict (from JSON) or a tuple/list of (d, n).
    if isinstance(private_key, dict):
        d = int(private_key["d"])
        n = int(private_key["n"])
    else:
        d, n = private_key
        d = int(d)
        n = int(n)

    print(f"Descriptografando: {input_path}")
    
    with open(input_path, 'r') as f_in, open(output_path, 'wb') as f_out:
        for line in f_in:
            length_str, c_str = line.strip().split(":", 1)
            chunk_len = int(length_str)
            c = int(c_str)

            m = pow(c, d, n)

            # Restore leading zeros by using the original chunk length.
            chunk = m.to_bytes(chunk_len, byteorder='big')

            f_out.write(chunk)


def generate_keys():
    print(f"Gerando chaves de {BIT_LENGTH} bits...")

    p = generate_prime(BIT_LENGTH // 2)
    q = generate_prime(BIT_LENGTH // 2)

    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = modular_inverter(e, phi)

    print("\nChaves geradas:")
    print(f"- Pública: ({e}, {n})")
    print(f"- Privada: ({d}, {n})\n")

    return (e, n), (d, n)


def save_keys(e, d, n):
    os.makedirs("keys", exist_ok=True)

    public_key_data = {
        "e": e,
        "n": n
    }

    private_key_data = {
        "d": d,
        "n": n
    }

    with open(PUBLIC_KEY_PATH, "w") as f:
        json.dump(public_key_data, f)

    with open(PRIVATE_KEY_PATH, "w") as f:
        json.dump(private_key_data, f)

    print("\nChaves salvas")
