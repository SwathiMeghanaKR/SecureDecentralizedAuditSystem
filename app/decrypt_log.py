from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad

def decrypt_audit_log(enc_log_path, encrypted_key_path, private_key_path):
    # Load encrypted AES key
    rsa_key = RSA.import_key(open(private_key_path).read())
    cipher_rsa = PKCS1_OAEP.new(rsa_key)

    with open(encrypted_key_path, 'rb') as f:
        encrypted_key = f.read()
    aes_key = cipher_rsa.decrypt(encrypted_key)

    # Load encrypted log file
    with open(enc_log_path, 'rb') as f:
        data = f.read()
    iv = data[:16]
    ciphertext = data[16:]

    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher_aes.decrypt(ciphertext), AES.block_size)

    print("✅ Decrypted Audit Log:")
    print(plaintext.decode())

# Example use
decrypt_audit_log(
    enc_log_path='data/audit_log.enc',
    encrypted_key_path='data/aes_key_for_auditor1.bin',
    private_key_path='keys/auditor1_private.pem'
)
