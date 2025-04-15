import json, hashlib, time
from app.models import AuditRecord
from app.auth import sign_data

def hash_record(data):
    return hashlib.sha256(data.encode()).hexdigest()

def create_audit_record(patient_id, user_id, action, private_key):
    with open('data/audit_log.json', 'r+') as f:
        log = json.load(f)
        previous_hash = log[-1]['record_hash'] if log else "0" * 64
        timestamp = time.strftime('%Y-%m-%dT%H:%M:%S')
        raw_data = f"{timestamp}{patient_id}{user_id}{action}{previous_hash}"
        record_hash = hash_record(raw_data)
        signature = sign_data(private_key, raw_data)
        record = AuditRecord(timestamp, patient_id, user_id, action, previous_hash, record_hash, signature)
        log.append(record.__dict__)
        f.seek(0)
        json.dump(log, f, indent=4)
