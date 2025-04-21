# from app.audit import create_audit_record
# from app.auth import verify_signature

# from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# import json

# main = Blueprint('main', __name__)

# @main.route('/')
# def index():
#     return render_template("index.html")

# # @main.route('/logs')
# # def view_logs():
# #     with open('data/audit_log.json') as f:
# #         logs = json.load(f)
# #     return render_template("view_logs.html", logs=logs)

# @main.route('/add', methods=['GET', 'POST'])
# def add_log():
#     if request.method == 'POST':
#         user_id = request.form['user_id']
#         patient_id = request.form['patient_id']
#         action = request.form['action']
#         create_audit_record(patient_id, user_id, action, f'keys/{user_id}_private.pem')
#         return redirect(url_for('main.view_logs'))
#     return render_template("add_record.html")


# ####

# def load_users():
#     with open('data/users.json') as f:
#         return json.load(f)

# def get_user_role(user_id):
#     users = load_users()
#     for user in users:
#         if user['user_id'] == user_id:
#             return user['role']
#     return None
# @main.route('/login/<role>', methods=['GET', 'POST'])
# def login(role):
#     if request.method == 'POST':
#         user_id = request.form['user_id']
#         role = role.lower()
#         for user in load_users():
#             if user['user_id'] == user_id and user['role'] == role:
#                 session['user_id'] = user_id
#                 session['role'] = role
#                 return redirect(url_for('main.dashboard'))
#         flash("Invalid user ID or role.")
#     return render_template("login.html", role=role)

# @main.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('main.login'))

# @main.route('/dashboard')
# def dashboard():
#     if 'user_id' not in session:
#         return redirect(url_for('main.index'))

#     user_id = session['user_id']
#     role = session['role']
#     return render_template("dashboard.html", user_id=user_id, role=role)

# @main.route('/logs', methods=['GET', 'POST'])
# def view_logs():
#     if 'user_id' not in session:
#         return redirect(url_for('main.login'))

#     user_id = session['user_id']
#     role = session['role']
#     patient_filter = request.args.get('patient_id') or request.form.get('patient_id')

#     with open('data/audit_log.json') as f:
#         logs = json.load(f)

#     if role == 'patient':
#         logs = [log for log in logs if log['patient_id'] == user_id]
#     elif patient_filter:
#         logs = [log for log in logs if log['patient_id'] == patient_filter]

#     return render_template("view_logs.html", logs=logs, patient_id=patient_filter, user_id=user_id, role=role)
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import json
from datetime import datetime
from app.models import add_audit_record, load_audit_log

main = Blueprint('main', __name__)

# Load users from users.json
def load_users():
    with open('data/users.json') as f:
        return json.load(f)

# Get user role by user_id
def get_user_role(user_id):
    for user in load_users():
        if user['user_id'] == user_id:
            return user['role']
    return None

# Landing page
@main.route('/')
def index():
    return render_template("index.html")

# Login route per role
@main.route('/login/<role>', methods=['GET', 'POST'])
def login(role):
    role = role.lower()
    if request.method == 'POST':
        user_id = request.form['user_id']
        users = load_users()
        for user in users:
            if user['user_id'] == user_id and user['role'] == role:
                session['user_id'] = user_id
                session['role'] = role
                return redirect(url_for('main.dashboard'))
        flash("Invalid user ID or role.")
    return render_template("login.html", role=role)

# Logout route
@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

# Dashboard after login
@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main.index'))
    return render_template("dashboard.html", user_id=session['user_id'], role=session['role'])

# Doctor: Add audit record
@main.route('/add', methods=['GET', 'POST'])
def add_record():
    if 'user_id' not in session or session['role'] != 'doctor':
        flash("Only doctors can add audit records.")
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        user_id = session['user_id']
        patient_id = request.form['patient_id']
        action = request.form['action']
        timestamp = datetime.now().isoformat()

        add_audit_record(user_id, patient_id, action, timestamp)
        flash("Audit record added successfully.")
        return redirect(url_for('main.dashboard'))

    return render_template("add_record.html")

# View logs route (auditor sees all; patient sees their own)
@main.route('/logs', methods=['GET', 'POST'])
def view_logs():
    if 'user_id' not in session:
        return redirect(url_for('main.index'))

    user_id = session['user_id']
    role = session['role']
    logs = load_audit_log()

    patient_filter = request.args.get('patient_id') or request.form.get('patient_id')

    if role == 'patient':
        logs = [log for log in logs if log['patient_id'] == user_id]
    elif role == 'auditor' and patient_filter:
        logs = [log for log in logs if log['patient_id'] == patient_filter]
    elif role == 'doctor' and patient_filter:
        logs = [log for log in logs if log['patient_id'] == patient_filter]

    return render_template("view_logs.html", logs=logs, user_id=user_id, role=role, patient_id=patient_filter)
