from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
from flask_jwt_extended import create_access_token
import requests
import json
from .models import Model, Dataset


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

@main.route('/api/create-project', methods=['POST'])
def submit_training():
    data = request.json
    print("프론트엔드에서 받은 프로젝트 데이터:", data)
    
    # 다른 백엔드 URL
    other_backend_url = "http://163.180.117.160:8000/training"

    # 요청 전송 확인 메시지 출력
    print("다른 백엔드로 요청을 전송합니다:", other_backend_url)

    response = requests.post(other_backend_url, json=data)
    
    # 응답 상태 코드 로깅
    print("Status Code:", response.status_code)
    
    # 응답 헤더 로깅
    print("Response Headers:", response.headers)

    # 원본 응답 내용 로깅
    if response.content:
        print("Raw Response Content:", response.content)

        # 응답이 JSON 형식인 경우 JSON 데이터 파싱 후 로깅
        if response.headers.get('Content-Type') == 'application/json':
            try:
                response_data = response.json()
                print("다른 백엔드에서 받은 응답 데이터:", response_data)
                
                # 성공 응답 반환
                return jsonify(response_data), 200
            except ValueError as e:
                # JSON 파싱 오류 처리
                print("JSON 파싱 오류:", e)
                return jsonify({"message": "다른 백엔드로부터 유효하지 않은 JSON 응답을 받았습니다."}), 500
        else:
            # JSON이 아닌 응답 처리
            print("다른 백엔드에서 JSON 형식이 아닌 응답을 받음")
            return jsonify({"message": "다른 백엔드로부터 JSON 형식이 아닌 응답을 받았습니다."}), 500
    else:
        # 빈 응답 처리
        print("다른 백엔드로부터 빈 응답을 받음")
        return jsonify({"message": "다른 백엔드로부터 빈 응답을 받았습니다."}), 500

@main.route('/api/data/models', methods=['GET'])
def get_models():
    # 데이터베이스에서 모든 모델 정보를 조회
    models = Model.query.all()
    # 조회한 모델 정보를 JSON 형식으로 변환
    models_data = [{
        'model_id': model.model_id,
        'name': model.name,
        'description': model.description
    } for model in models]
    # JSON 데이터로 응답
    return jsonify(models_data)

@main.route('/api/data/datasets', methods=['GET'])
def get_datasets():
    # 데이터베이스에서 모든 데이터셋 정보를 조회
    datasets = Dataset.query.all()
    # 조회한 데이터셋 정보를 JSON 형식으로 변환
    datasets_data = [{
        'dataset_id': dataset.dataset_id,
        'name': dataset.name,
        'description': dataset.description,
    } for dataset in datasets]
    # JSON 데이터로 응답
    return jsonify(datasets_data)

# @main.route('/api/create-project', methods=['POST'])
# def submit_training():
#     # 전송된 데이터를 받음
#     data = request.json
#     print("프론트엔드에서 받은 프로젝트 데이터:", data)
    
#     # 다른 백엔드 URL
#     other_backend_url = "http://163.180.117.160:8000/training"
    
#     # `requests`를 사용하여 다른 백엔드로 데이터 전송
#     try:
#         response = requests.post(other_backend_url, json=data)
#         response_data = response.json()
#         print("Response from other backend:", response_data)
        
#         # Check if the response from the other backend indicates success
#         if response.status_code == 200 and response_data.get('success'):
#             # 성공적으로 데이터를 전송했을 때의 처리
#             return jsonify({"message": "Data successfully submitted to other backend.", "id": response_data.get('id')}), 200
#         else:
#             #  실패했을 때의 처리 (either due to a non-200 status code or success being False)
#             return jsonify({"message": "Failed to submit data to other backend.", "error": response_data.get('message')}), response.status_code
#     except requests.exceptions.RequestException as e:
#         # Handling exceptions when sending request to other backend fails
#         print(e)
#         return jsonify({"message": "Failed to connect to other backend."}), 500


# @main.route('/api/create-project', methods=['POST'])
# def create_project():
#     # 전송된 데이터를 받음
#     data = request.json
#     print("Received project data:", data)
    
#     # 데이터 처리 로직 (예시)
#     # 여기에서는 단순히 받은 데이터를 그대로 반환하고 있습니다.
#     return jsonify(data), 200
    
# @main.route('/api/create-project', methods=['POST'])
# def submit_training():
#     data = request.json
#     # 다른 백엔드 URL
#     other_backend_url = "http://163.180.117.160:8000/training"

#     # `requests`를 사용하여 다른 백엔드로 데이터 전송
#     response = requests.post(other_backend_url, json=data)

#     if response.status_code == 200:
#         # 성공적으로 데이터를 전송했을 때의 처리
#         return jsonify({"message": "Data successfully submitted to other backend."}), 200
#     else:
#         # 실패했을 때의 처리
#         return jsonify({"message": "Failed to submit data to other backend."}), response.status_code
    
    