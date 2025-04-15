from auth import generate_keys

# Generate key pairs for some sample users
users = ['admin', 'doctor1', 'auditor1']
for user_id in users:
    generate_keys(user_id)

print("Keys generated in /keys/")
