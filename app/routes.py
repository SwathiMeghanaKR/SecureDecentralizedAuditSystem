from app.audit import create_audit_record
from app.auth import verify_signature

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html")

# @main.route('/logs')
# def view_logs():
#     with open('data/audit_log.json') as f:
#         logs = json.load(f)
#     return render_template("view_logs.html", logs=logs)

@main.route('/add', methods=['GET', 'POST'])
def add_log():
    if request.method == 'POST':
        user_id = request.form['user_id']
        patient_id = request.form['patient_id']
        action = request.form['action']
        create_audit_record(patient_id, user_id, action, f'keys/{user_id}_private.pem')
        return redirect(url_for('main.view_logs'))
    return render_template("add_record.html")

####

def load_users():
    with open('data/users.json') as f:
        return json.load(f)

def get_user_role(user_id):
    users = load_users()
    for user in users:
        if user['user_id'] == user_id:
            return user['role']
    return None
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        role = get_user_role(user_id)
        if role:
            session['user_id'] = user_id
            session['role'] = role
            return redirect(url_for('main.view_logs'))
        else:
            flash("User not found.")
    return render_template("login.html")
@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))
@main.route('/logs', methods=['GET', 'POST'])
def view_logs():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    role = session['role']
    patient_filter = request.args.get('patient_id') or request.form.get('patient_id')

    with open('data/audit_log.json') as f:
        logs = json.load(f)

    if role == 'patient':
        logs = [log for log in logs if log['patient_id'] == user_id]
    elif patient_filter:
        logs = [log for log in logs if log['patient_id'] == patient_filter]

    return render_template("view_logs.html", logs=logs, patient_id=patient_filter, user_id=user_id, role=role)
