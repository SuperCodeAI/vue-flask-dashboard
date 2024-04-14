from app.extensions import db
from app.models import Model

def add_model_data():
    # 모델 데이터 정의
    models_to_add = [
        {
            "name": "Convolutional Neural Network(CNN)",
            "description": "이미지와 같은 격자형 토폴로지를 가진 데이터를 처리하는 데 주로 사용되는 딥러닝 모델의 한 유형입니다. CNN은 데이터의 로컬 특징에 필터를 적용하는 컨볼루션 레이어를 사용하여 이미지 및 비디오 인식, 이미지 분류, 의료 이미지 분석과 같은 작업에서 효과적인 특징 추출 및 인식을 가능하게 합니다."
        },
        {
            "name": "Long Short-Term Memory(LSTM)",
            "description": "언어 모델링, 음성 인식, 시계열 예측 등 시퀀스를 다루는 작업에 사용됩니다. 데이터 시퀀스의 장기 의존성을 포착할 수 있는 순환 신경망의 일종입니다."
        }
    ]
    # 데이터베이스에 각 모델 추가
    for model_data in models_to_add:
        model = Model(name=model_data["name"], description=model_data["description"])
        db.session.add(model)
    
    # 변경사항을 데이터베이스에 커밋
    db.session.commit()

# 함수 호출하여 데이터 추가
add_model_data()