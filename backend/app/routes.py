from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
from flask_jwt_extended import create_access_token

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
        return jsonify(access_token=access_token), 200
    else:
        # 실패한 경우
        return jsonify({'message': 'Invalid credentials.'}), 401