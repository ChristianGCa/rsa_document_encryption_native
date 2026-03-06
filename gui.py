import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from crypto_utils import (
    decrypt_file,
    encrypt_file,
    generate_keys,
    load_private_key,
    load_public_key,
    save_keys,
)

DEFAULT_PUBLIC_KEY_PATH = "keys/public_key.json"
DEFAULT_PRIVATE_KEY_PATH = "keys/private_key.json"


def _safe_load_json(text):
    try:
        return json.loads(text)
    except Exception as e:
        raise ValueError(f"JSON inválido: {e}")


class RSAApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RSA Document Encryption")
        self.geometry("1920x1080")

        self._build_ui()
        self._load_keys_from_disk()

    def _build_ui(self):
        pad = 8
        frame_top = tk.Frame(self)
        frame_top.pack(fill="x", padx=pad, pady=(pad, 0))

        # Public key
        pub_frame = tk.LabelFrame(frame_top, text="Chave Pública (e, n)")
        pub_frame.pack(fill="x", padx=pad, pady=pad)

        self.pub_text = scrolledtext.ScrolledText(pub_frame, height=5)
        self.pub_text.pack(fill="x", padx=pad, pady=(0, pad))

        pub_btn_frame = tk.Frame(pub_frame)
        pub_btn_frame.pack(fill="x", padx=pad)

        tk.Button(pub_btn_frame, text="Carregar (keys/public_key.json)", command=self._load_public_key).pack(side="left")
        tk.Button(pub_btn_frame, text="Salvar", command=self._save_public_key).pack(side="left", padx=(8, 0))

        # Private key
        priv_frame = tk.LabelFrame(frame_top, text="Chave Privada (d, n)")
        priv_frame.pack(fill="x", padx=pad, pady=pad)

        self.priv_text = scrolledtext.ScrolledText(priv_frame, height=5)
        self.priv_text.pack(fill="x", padx=pad, pady=(0, pad))

        priv_btn_frame = tk.Frame(priv_frame)
        priv_btn_frame.pack(fill="x", padx=pad)

        tk.Button(priv_btn_frame, text="Carregar (keys/private_key.json)", command=self._load_private_key).pack(side="left")
        tk.Button(priv_btn_frame, text="Salvar", command=self._save_private_key).pack(side="left", padx=(8, 0))

        # Key generation
        gen_frame = tk.Frame(self)
        gen_frame.pack(fill="x", padx=pad, pady=(0, pad))

        tk.Button(gen_frame, text="Gerar novo par de chaves", command=self._generate_keys).pack(side="left")

        # Encryption/Decryption
        op_frame = tk.LabelFrame(self, text="Operações")
        op_frame.pack(fill="both", expand=True, padx=pad, pady=(0, pad))

        # Encrypt
        encrypt_frame = tk.LabelFrame(op_frame, text="Criptografar")
        encrypt_frame.pack(fill="x", padx=pad, pady=(pad, 0))

        self.encrypt_input_entry = self._build_file_selector(
            encrypt_frame, "Arquivo original:", "Escolher arquivo...", "", ""
        )
        self.encrypt_output_entry = self._build_file_selector(
            encrypt_frame, "Arquivo de saída:", "Salvar como...", "", ""
        )
        tk.Button(encrypt_frame, text="Criptografar", command=self._on_encrypt).pack(pady=(pad, 0))

        # Decrypt
        decrypt_frame = tk.LabelFrame(op_frame, text="Descriptografar")
        decrypt_frame.pack(fill="x", padx=pad, pady=(pad, 0))

        self.decrypt_input_entry = self._build_file_selector(
            decrypt_frame, "Arquivo criptografado:", "Escolher arquivo...", "", ""
        )
        self.decrypt_output_entry = self._build_file_selector(
            decrypt_frame, "Arquivo de saída:", "Salvar como...", "", ""
        )
        tk.Button(decrypt_frame, text="Descriptografar", command=self._on_decrypt).pack(pady=(pad, 0))

        # Status
        self.status = tk.StringVar(value="Pronto")
        status_label = tk.Label(self, textvariable=self.status, anchor="w")
        status_label.pack(fill="x", padx=pad, pady=(0, pad))

    def _build_file_selector(self, parent, label_text, button_text, entry_text, default_path):
        row = tk.Frame(parent)
        row.pack(fill="x", padx=8, pady=4)

        tk.Label(row, text=label_text, width=18, anchor="w").pack(side="left")
        entry = tk.Entry(row)
        entry.insert(0, default_path)
        entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        def pick():
            if "Salvar" in button_text or "saída" in label_text.lower():
                path = filedialog.asksaveasfilename(defaultextension="")
            else:
                path = filedialog.askopenfilename()
            if path:
                entry.delete(0, tk.END)
                entry.insert(0, path)

        btn = tk.Button(row, text=button_text, command=pick)
        btn.pack(side="right")

        return entry

    def _load_keys_from_disk(self):
        try:
            pub = load_public_key()
            self.pub_text.delete("1.0", tk.END)
            self.pub_text.insert(tk.END, json.dumps(pub, indent=2))
        except FileNotFoundError:
            pass

        try:
            priv = load_private_key()
            self.priv_text.delete("1.0", tk.END)
            self.priv_text.insert(tk.END, json.dumps(priv, indent=2))
        except FileNotFoundError:
            pass

    def _load_public_key(self):
        try:
            pub = load_public_key()
            self.pub_text.delete("1.0", tk.END)
            self.pub_text.insert(tk.END, json.dumps(pub, indent=2))
            self._set_status("Chave pública carregada.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar a chave pública:\n{e}")

    def _load_private_key(self):
        try:
            priv = load_private_key()
            self.priv_text.delete("1.0", tk.END)
            self.priv_text.insert(tk.END, json.dumps(priv, indent=2))
            self._set_status("Chave privada carregada.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar a chave privada:\n{e}")

    def _save_public_key(self):
        try:
            pub = _safe_load_json(self.pub_text.get("1.0", tk.END))
            if not all(k in pub for k in ("e", "n")):
                raise ValueError("A chave pública deve conter 'e' e 'n'.")
            os.makedirs(os.path.dirname(DEFAULT_PUBLIC_KEY_PATH), exist_ok=True)
            with open(DEFAULT_PUBLIC_KEY_PATH, "w") as f:
                json.dump({"e": pub["e"], "n": pub["n"]}, f)
            self._set_status("Chave pública salva.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar a chave pública:\n{e}")

    def _save_private_key(self):
        try:
            priv = _safe_load_json(self.priv_text.get("1.0", tk.END))
            if not all(k in priv for k in ("d", "n")):
                raise ValueError("A chave privada deve conter 'd' e 'n'.")
            os.makedirs(os.path.dirname(DEFAULT_PRIVATE_KEY_PATH), exist_ok=True)
            with open(DEFAULT_PRIVATE_KEY_PATH, "w") as f:
                json.dump({"d": priv["d"], "n": priv["n"]}, f)
            self._set_status("Chave privada salva.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar a chave privada:\n{e}")

    def _on_encrypt(self):
        try:
            pub = _safe_load_json(self.pub_text.get("1.0", tk.END))
            input_path = self.encrypt_input_entry.get().strip()
            output_path = self.encrypt_output_entry.get().strip()
            if not input_path or not output_path:
                raise ValueError("Selecione arquivo de entrada e saída.")
            encrypt_file(input_path, output_path, public_key=pub, save_keys_flag=False)
            self._set_status("Arquivo criptografado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível criptografar:\n{e}")

    def _on_decrypt(self):
        try:
            priv = _safe_load_json(self.priv_text.get("1.0", tk.END))
            input_path = self.decrypt_input_entry.get().strip()
            output_path = self.decrypt_output_entry.get().strip()
            if not input_path or not output_path:
                raise ValueError("Selecione arquivo de entrada e saída.")
            decrypt_file(input_path, output_path, priv)
            self._set_status("Arquivo descriptografado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível descriptografar:\n{e}")

    def _generate_keys(self):
        try:
            pub, priv = generate_keys()
            # Save to disk
            save_keys(pub[0], priv[0], pub[1])

            self.pub_text.delete("1.0", tk.END)
            self.pub_text.insert(tk.END, json.dumps({"e": pub[0], "n": pub[1]}, indent=2))
            self.priv_text.delete("1.0", tk.END)
            self.priv_text.insert(tk.END, json.dumps({"d": priv[0], "n": priv[1]}, indent=2))
            self._set_status("Chaves geradas e salvas.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível gerar chaves:\n{e}")

    def _set_status(self, text):
        self.status.set(text)


def main():
    app = RSAApp()
    app.mainloop()


if __name__ == "__main__":
    main()
