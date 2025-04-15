from flask import Blueprint, render_template, request, redirect, url_for
from app.audit import create_audit_record
from app.auth import verify_signature
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/logs')
def view_logs():
    with open('data/audit_log.json') as f:
        logs = json.load(f)
    return render_template("view_logs.html", logs=logs)

@main.route('/add', methods=['GET', 'POST'])
def add_log():
    if request.method == 'POST':
        user_id = request.form['user_id']
        patient_id = request.form['patient_id']
        action = request.form['action']
        create_audit_record(patient_id, user_id, action, f'keys/{user_id}_private.pem')
        return redirect(url_for('main.view_logs'))
    return render_template("add_record.html")
