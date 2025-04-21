import json
import os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

def encrypt_audit_log(json_data_path, output_path, public_key_path, aes_key_output_path):
    # Read existing audit data
    with open(json_data_path, 'r') as f:
        plaintext = f.read().encode()

    # Generate AES key
    aes_key = get_random_bytes(16)

    # Encrypt audit log using AES
    cipher_aes = AES.new(aes_key, AES.MODE_CBC)
    ciphertext = cipher_aes.encrypt(pad(plaintext, AES.block_size))

    # Save AES-encrypted log with IV
    with open(output_path, 'wb') as f:
        f.write(cipher_aes.iv + ciphertext)

    # Encrypt AES key using auditor's RSA public key
    rsa_key = RSA.import_key(open(public_key_path).read())
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    encrypted_key = cipher_rsa.encrypt(aes_key)

    # Save encrypted AES key
    with open(aes_key_output_path, 'wb') as f:
        f.write(encrypted_key)

    print("✅ Log encrypted and AES key secured with RSA.")

# Example use
encrypt_audit_log(
    json_data_path='data/audit_log.json',
    output_path='data/audit_log.enc',
    public_key_path='keys/auditor1_public.pem',
    aes_key_output_path='data/aes_key_for_auditor1.bin'
)
