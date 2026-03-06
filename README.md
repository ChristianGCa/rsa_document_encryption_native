# RSA Document Encryption

Este projeto implementa um simples esquema de encriptação e desencriptação de arquivos usando o algoritmo RSA em Python sem utilizar bibliotecas que não sejam as nativas do Python. A chave pública é usada para criptografar documentos e a chave privada para descriptografar.

## Estrutura do repositório

```
decrypt.py          # script para descriptografar usando chave privada
encrypt.py          # script para gerar chaves e criptografar um arquivo
main.py             # demo que chama encrypt_file e decrypt_file
crypto_utils/       # módulo com lógica RSA
    crypto_engine.py    # geração de chaves, encriptação e desencriptação de arquivos
    math_operations.py  # operações matemáticas auxiliares (primo, inverso modular)
docs/               # arquivos de exemplo e testes
keys/               # armazenamento das chaves geradas
```

## Como usar

1. **Instalação**
   - Este é um projeto Python puro e não possui dependências externas além da biblioteca padrão.

2. **Criptografar um arquivo**
   ```bash
   python encrypt.py
   ```
   - O script `encrypt.py` gera um par de chaves RSA, salva ambos em `keys/public_key.json` e `keys/private_key.json` e cria o arquivo cifrado (`.enc`).

3. **Descriptografar um arquivo**
   ```bash
   python decrypt.py
   ```
   - Forneça o caminho do arquivo criptografado e do arquivo de saída, além da chave privada. O exemplo no script já contém a lógica de leitura das chaves.

4. **Demo completo**
   ```bash
   python main.py
   ```
   - Executa a sequência de geração, encriptação, leitura das chaves e desencriptação, mostrando o texto restaurado.

5. **Interface gráfica (Tkinter)**
   ```bash
   python gui.py
   ```
   - Abre uma janela onde é possível gerar chaves, editar as chaves pública/privada, criptografar e descriptografar arquivos em passos separados.

## Componentes principais

- `crypto_utils/crypto_engine.py` - funções centrais de RSA: geração de chaves, salvamento, encriptação e desencriptação em blocos.
- `crypto_utils/math_operations.py` - funções matemáticas necessárias (miller-rabin, inverso modular, geração de primos).

## Observações

- O tamanho das chaves é fixo em 1024 bits (configurável via constante `BIT_LENGTH`).
- A chave pública nunca é necessária para desencriptação;
  apenas a privada é usada. O módulo `n` é compartilhado entre ambas.
- Este código é educativo e não para uso em produção sem melhorias de segurança (padding, verificação de integridade, etc.).

## Limpeza de artefatos

Para remover arquivos gerados e chaves, execute:

```bash
python del.py
```