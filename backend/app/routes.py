from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
from flask_jwt_extended import create_access_token
import requests

main = Blueprint('main', __name__)

@main.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name') 
    email = data.get('email')
    password = data.get('password')
    
    # 이미 등록된 이메일인지 확인
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'message': '기존의 존재하는 이메일입니다.'}), 409
    
    # 새로운 사용자 생성
    new_user = User(name=name, email=email, password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully.'}), 201

@main.route('/api/signin', methods=['POST'])
def signin():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # 사용자 조회
    user = User.query.filter_by(email=email).first()
    
    # 사용자가 존재하고 비밀번호가 맞는 경우
    if user and check_password_hash(user.password_hash, password):
        # 토큰 생성
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token, email=email), 200
    else:
        # 실패한 경우
        return jsonify({'message': 'Invalid credentials.'}), 401

    
@main.route('/api/submit-training', methods=['POST'])
def submit_training():
    data = request.json
    # 다른 백엔드 URL
    other_backend_url = "http://otherbackend.example.com/api/receive-training"

    # `requests`를 사용하여 다른 백엔드로 데이터 전송
    response = requests.post(other_backend_url, json=data)

    if response.status_code == 200:
        # 성공적으로 데이터를 전송했을 때의 처리
        return jsonify({"message": "Data successfully submitted to other backend."}), 200
    else:
        # 실패했을 때의 처리
        return jsonify({"message": "Failed to submit data to other backend."}), response.status_code
    
    