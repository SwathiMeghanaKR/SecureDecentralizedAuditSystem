import json, hashlib

def hash_record(r):
    raw = f"{r['timestamp']}{r['patient_id']}{r['user_id']}{r['action']}{r['previous_hash']}"
    return hashlib.sha256(raw.encode()).hexdigest()

with open("data/audit_log.json") as f:
    logs = json.load(f)

for i in range(1, len(logs)):
    expected = logs[i]['previous_hash']
    actual = logs[i-1]['record_hash']
    if expected != actual:
        print(f"Tampering detected at record {i}")
        break
else:
    print("Audit chain is valid.")