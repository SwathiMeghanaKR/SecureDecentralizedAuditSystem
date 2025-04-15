from dataclasses import dataclass

@dataclass
class User:
    user_id: str
    role: str  # 'admin', 'doctor', 'auditor'

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
