# from dataclasses import dataclass

# @dataclass
# class User:
#     user_id: str
#     role: str  # 'admin', 'doctor', 'auditor'

# @dataclass
# class Patient:
#     patient_id: str
#     name: str

# @dataclass
# class AuditRecord:
#     timestamp: str
#     patient_id: str
#     user_id: str
#     action: str
#     previous_hash: str
#     record_hash: str
#     signature: str
from dataclasses import dataclass
import json
import os
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

AUDIT_LOG_FILE = 'data/audit_log.json'
KEYS_FOLDER = 'keys'

# Data models
@dataclass
class User:
    user_id: str
    role: str  # 'doctor', 'auditor', 'patient'

@dataclass
class Patient:
    patient_id: str
    name: str

@dataclass
class AuditRecord:
    timestamp: str
    patient_id: str
    user_id: str
    action: str
    previous_hash: str
    record_hash: str
    signature: str

# Load audit log from file
def load_audit_log():
    if not os.path.exists(AUDIT_LOG_FILE):
        return []
    with open(AUDIT_LOG_FILE, 'r') as f:
        return json.load(f)

# Save audit log to file
def save_audit_log(logs):
    with open(AUDIT_LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

# Compute SHA-256 hash of a record
def compute_hash(record):
    record_str = json.dumps(record, sort_keys=True).encode()
    return hashlib.sha256(record_str).hexdigest()

# Add and sign a new audit record
def add_audit_record(user_id, patient_id, action, timestamp):
    logs = load_audit_log()
    previous_hash = compute_hash(logs[-1]) if logs else None

    record = {
        "timestamp": timestamp,
        "user_id": user_id,
        "patient_id": patient_id,
        "action": action,
        "previous_hash": previous_hash
    }

    # Hash the record
    record_hash = compute_hash(record)
    record["record_hash"] = record_hash

    # Sign the record hash
    private_key_path = os.path.join(KEYS_FOLDER, f"{user_id}_private.pem")
    if not os.path.exists(private_key_path):
        raise FileNotFoundError(f"Private key for {user_id} not found.")

    key = RSA.import_key(open(private_key_path).read())
    h = SHA256.new(record_hash.encode())
    signature = pkcs1_15.new(key).sign(h)
    record["signature"] = signature.hex()

    # Append and save
    logs.append(record)
    save_audit_log(logs)
