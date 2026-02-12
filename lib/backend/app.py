from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from models import db, User  # Make sure models.py exists in the same folder

# ----- Upload folder -----
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----- Flask App -----
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)

# ----- Create tables and add test user -----
with app.app_context():
    db.create_all()

    # Add a test user if not exists
    if not User.query.filter_by(email="student@email.com").first():
        user = User(email="student@email.com")
        user.set_password("123456")  # Test password
        db.session.add(user)
        db.session.commit()
        print("Test user added")

# ===== Authentication =====
@app.route('/register', methods=['POST', 'OPTIONS'])
def register():
    print(f"Request method: {request.method}")
    print(f"Request headers: {dict(request.headers)}")
    print(f"Request body: {request.data}")
    
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.json
        print(f"Register request data: {data}")
        
        if not data:
            print("ERROR: No JSON data")
            return jsonify({'error': 'No JSON data provided'}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not email or not password:
            print(f"ERROR: Missing email={email} or password={password}")
            return jsonify({'error': 'Email and password required'}), 400

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"ERROR: Email {email} already exists")
            return jsonify({'error': 'Email already exists'}), 400

        user = User(
            email=email,
            name=data.get('name', 'Student Name'),
            college=data.get('college', 'ABC College'),
            dept=data.get('dept', 'Computer Science'),
            year=data.get('year', '3rd Year'),
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"SUCCESS: User {email} created")
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        print(f"ERROR in register: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        return jsonify({'message': 'Login successful', 'user_id': user.id})
    return jsonify({'error': 'Invalid credentials'}), 401

# ===== Profile =====
@app.route('/profile/<int:user_id>', methods=['GET', 'PUT'])
def profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if request.method == 'GET':
        return jsonify({
            'name': user.name,
            'email': user.email,
            'college': user.college,
            'dept': user.dept,
            'year': user.year
        })
    else:  # PUT
        data = request.json
        user.name = data.get('name', user.name)
        user.college = data.get('college', user.college)
        user.dept = data.get('dept', user.dept)
        user.year = data.get('year', user.year)
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'})

# ===== Upload Note =====
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({'message': 'File uploaded successfully', 'filename': filename})

# ===== Download Note =====
@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# ===== List Notes =====
@app.route('/notes', methods=['GET'])
def list_notes():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({'files': files})

# ===== Run the app =====
if __name__ == '__main__':
    app.run(debug=True)
