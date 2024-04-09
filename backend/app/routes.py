from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Model, Dataset, Project
from flask_jwt_extended import create_access_token , get_jwt_identity, jwt_required
import requests
import json
from .models import Model, Dataset
from sqlalchemy.exc import SQLAlchemyError

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
@jwt_required()
def submit_training():
    current_user_email = get_jwt_identity()
    #current_user_email = "123123@123.com"
    current_user = User.query.filter_by(email=current_user_email).first()
    
    current_app.logger.info(f"유저 ID: {current_user}")
    
    if not current_user:
        return jsonify({"message": "사용자를 찾을 수 없습니다."}), 404
    
    data = request.json
    print("프론트엔드에서 받은 프로젝트 데이터:", data)
    
    model = Model.query.get(data['model'])
    dataset = Dataset.query.get(data['dataset'])
    
    current_app.logger.info(f"Model: {model}, Dataset: {dataset}")
    
    if not model or not dataset:
        return jsonify({"message": "모델 또는 데이터셋을 찾을 수 없습니다."}), 404


    try:
        new_project = Project(
            user_id=current_user.user_id,
            model_id=model.model_id,
            dataset_id=dataset.dataset_id,
            status="생성 요청"
        )
        db.session.add(new_project)
        db.session.commit()

        current_app.logger.info(f"프로젝트 생성 성공: Project ID {new_project.id}")

        modified_data = {
            "id": new_project.id,
            "model": model.model_id,  # 여기는 정수형 ID
            "dataset": dataset.dataset_id,  # 여기는 정수형 ID
            "hyperparameters": data['hyperparameters'],
            "nodes": data['nodes']
        }
        current_app.logger.info(f"수정된 파일: {modified_data}")

        other_backend_url = "http://163.180.117.160:8000/training"
        response = requests.post(other_backend_url, json=modified_data)

        if response.status_code == 200:
            new_project.status = "학습 중"
            db.session.commit()
            return jsonify({"message": "다른 백엔드로 프로젝트 정보가 성공적으로 전송되었습니다.", "project_id": new_project.id}), 200
        else:
            return jsonify({"message": "다른 백엔드로 프로젝트 정보 전송에 실패하였습니다."}), response.status_code
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error during project creation: {e}")
        return jsonify({"message": "프로젝트 생성 중 오류가 발생했습니다."}), 500
    

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

@main.route('/api/reset-db', methods=['POST'])
def reset_database():
    try:
        # 모든 프로젝트 데이터를 삭제합니다.
        num_rows_deleted = db.session.query(Project).delete()
        db.session.commit()
        
        # 성공 메시지와 함께 삭제된 행의 수를 반환합니다.
        return jsonify({"message": "Database reset successfully.", "rows_deleted": num_rows_deleted}), 200
    except Exception as e:
        # 에러 발생 시 롤백합니다.
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@main.route('/api/data/projects', methods=['POST'])
@jwt_required()
def fetch_projects():
    # 현재 로그인한 사용자의 이메일을 JWT 토큰에서 가져옵니다.
    current_user_email = get_jwt_identity()
    request_data = request.json
    email_from_request = request_data.get('email')

    # JWT 토큰에서 추출한 이메일과 요청에서 받은 이메일이 일치하는지 확인합니다.
    if current_user_email != email_from_request:
        return jsonify({"error": "Unauthorized access"}), 401

    # User 테이블에서 사용자의 이메일을 사용하여 사용자 정보를 조회합니다.
    user = User.query.filter_by(email=current_user_email).first()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    # Project 테이블에서 해당 사용자의 모든 프로젝트를 조회합니다.
    projects = Project.query.filter_by(user_id=user.user_id).all()
    projects_data = []

    for project in projects:
        model = Model.query.get(project.model_id)
        dataset = Dataset.query.get(project.dataset_id)

        projects_data.append({
            "id": project.id,
            "model_name": model.name if model else "Model not found",
            "dataset_name": dataset.name if dataset else "Dataset not found",
            "status": project.status,
            "created_at": project.created_at.strftime("%Y-%m-%d %H:%M:%S") if project.created_at else "N/A",
            "result": project.result
        })
    print(projects_data)
    return jsonify(projects_data)