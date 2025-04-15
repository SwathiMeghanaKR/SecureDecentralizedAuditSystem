from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def generate_keys(user_id):
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open(f"keys/{user_id}_private.pem", "wb") as f:
        f.write(private_key)

    with open(f"keys/{user_id}_public.pem", "wb") as f:
        f.write(public_key)

def sign_data(private_key_path, data):
    key = RSA.import_key(open(private_key_path).read())
    h = SHA256.new(data.encode())
    return pkcs1_15.new(key).sign(h).hex()

def verify_signature(public_key_path, data, signature_hex):
    key = RSA.import_key(open(public_key_path).read())
    h = SHA256.new(data.encode())
    try:
        pkcs1_15.new(key).verify(h, bytes.fromhex(signature_hex))
        return True
    except (ValueError, TypeError):
        return False
