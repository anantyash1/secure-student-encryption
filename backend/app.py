from flask import Flask, jsonify, request
from flask_cors import CORS
from cryptography.fernet import Fernet
import json
import base64
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to connect

DATA_FILE = '../students.json'  # Path to root JSON
KEY_FILE = 'secret.key'

def load_key():
    if os.path.exists(KEY_FILE):
        return open(KEY_FILE, 'rb').read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
        return key

key = load_key()
fernet = Fernet(key)

def load_students():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_students(students):
    with open(DATA_FILE, 'w') as f:
        json.dump(students, f, indent=2)

@app.route('/students', methods=['GET'])
def get_students():
    students = load_students()
    # Decrypt on-the-fly for display if encrypted
    for student in students:
        if student['encrypted'] and student['data']:
            try:
                encrypted_bytes = base64.urlsafe_b64decode(student['data'].encode())
                decrypted = fernet.decrypt(encrypted_bytes)
                student['profile'] = json.loads(decrypted.decode())
            except:
                student['profile'] = {'error': 'Decryption failed'}
        else:
            student['profile'] = {k: v for k, v in student.items() if k not in ['encrypted', 'data']}
    return jsonify(students)

@app.route('/students', methods=['POST'])
def add_student():
    new_student = request.json
    students = load_students()
    new_id = max(s['id'] for s in students) + 1 if students else 1
    new_student['id'] = new_id
    new_student['encrypted'] = False
    new_student['data'] = None
    # Auto-encrypt if requested
    if new_student.get('auto_encrypt', False):
        profile = {k: v for k, v in new_student.items() if k not in ['encrypted', 'data', 'auto_encrypt']}
        profile_json = json.dumps(profile).encode()
        encrypted = fernet.encrypt(profile_json)
        new_student['data'] = base64.urlsafe_b64encode(encrypted).decode()
        new_student['encrypted'] = True
    students.append(new_student)
    save_students(students)
    return jsonify({'message': 'Student added successfully', 'student': new_student})

@app.route('/encrypt/<int:student_id>', methods=['POST'])
def encrypt_student(student_id):
    students = load_students()
    student = next((s for s in students if s['id'] == student_id), None)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    if student['encrypted']:
        return jsonify({'error': 'Already encrypted'}), 400
    
    profile = {k: v for k, v in student.items() if k not in ['encrypted', 'data']}
    profile_json = json.dumps(profile).encode()
    encrypted = fernet.encrypt(profile_json)
    student['data'] = base64.urlsafe_b64encode(encrypted).decode()
    student['encrypted'] = True
    save_students(students)
    return jsonify({'message': 'Encrypted successfully'})

@app.route('/decrypt/<int:student_id>', methods=['POST'])
def decrypt_student(student_id):
    students = load_students()
    student = next((s for s in students if s['id'] == student_id), None)
    if not student or not student['encrypted']:
        return jsonify({'error': 'Not encrypted or not found'}), 400
    
    try:
        encrypted_bytes = base64.urlsafe_b64decode(student['data'].encode())
        decrypted = fernet.decrypt(encrypted_bytes)
        profile = json.loads(decrypted.decode())
        student['data'] = None
        student['encrypted'] = False
        # Restore original fields
        for k, v in profile.items():
            student[k] = v
        save_students(students)
        return jsonify({'message': 'Decrypted successfully'})
    except:
        return jsonify({'error': 'Decryption failed'}), 400

@app.route('/bulk-encrypt', methods=['POST'])
def bulk_encrypt():
    ids = request.json.get('ids', [])
    students = load_students()
    encrypted_count = 0
    for student_id in ids:
        student = next((s for s in students if s['id'] == student_id), None)
        if student and not student['encrypted']:
            profile = {k: v for k, v in student.items() if k not in ['encrypted', 'data']}
            profile_json = json.dumps(profile).encode()
            encrypted = fernet.encrypt(profile_json)
            student['data'] = base64.urlsafe_b64encode(encrypted).decode()
            student['encrypted'] = True
            encrypted_count += 1
    save_students(students)
    return jsonify({'message': f'Encrypted {encrypted_count} students successfully'})

@app.route('/bulk-decrypt', methods=['POST'])
def bulk_decrypt():
    ids = request.json.get('ids', [])
    students = load_students()
    decrypted_count = 0
    for student_id in ids:
        student = next((s for s in students if s['id'] == student_id), None)
        if student and student['encrypted']:
            try:
                encrypted_bytes = base64.urlsafe_b64decode(student['data'].encode())
                decrypted = fernet.decrypt(encrypted_bytes)
                profile = json.loads(decrypted.decode())
                student['data'] = None
                student['encrypted'] = False
                for k, v in profile.items():
                    student[k] = v
                decrypted_count += 1
            except:
                pass  # Skip failed decryptions
    save_students(students)
    return jsonify({'message': f'Decrypted {decrypted_count} students successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)