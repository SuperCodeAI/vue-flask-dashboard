from app.extensions import db
from app.models import Dataset

def add_dataset_data():
    # Define the model data to be added
    dataset_data = [
        {
            "name": "ImageNet",
            "description": "ImageNet은 20,000개 이상의 카테고리로 분류된 1,400만 개 이상의 주석이 달린 이미지가 포함하고 있는 대규모 데이터셋입니다. 데이터셋이 가지고 있는 다양성과 규모로 잘 알려져 있어 이미지 인식 모델을 훈련하고 평가하기 위한 포괄적인 데이터 세트입니다."
        },
        {
            "name": "COCO (Common Objects in Context)",
            "description": "COCO  4세 어린이가 쉽게 인식할 수 있는 91가지 개체 유형을 다루는 200,000개 이상의 라벨이 있는 330,000개 이상의 이미지가 포함되어 있습니다. 자연 환경에서 객체를 감지하고 분할하도록 설계되었으며 객체 감지, 분할, 캡션 등 다양한 컴퓨터 비전 작업을 지원합니다. 객체 컨텍스트와 공간 관계에 대한 이해가 필요한 고급 컴퓨터 비전 모델을 교육하는 데 필수적인 데이터셋입니다." },
        {
            "name": "Cityscapes",
            "description": "Cityscapes는 다양한 계절, 기상 조건, 주간 동안 50개 도시의 거리 장면을 녹화한 다양한 비디오 데이터가 ​​포함되어 있습니다. 데이터 세트는 다양한 유형의 차량, 보행자, 도로, 건물 등을 포함한 30개 클래스에 대한 고품질 픽셀 수준 주석을 미세한 주석이 있는 5,000개의 이미지와 거친 주석이 있는 20,000개의 이미지로 제공합니다. 이 데이터 세트는 의미론적 분할, 객체 감지, 인스턴스 분할 등 자율 주행 및 도시 장면 이해와 관련된 작업에 특히 유용합니다."
        }
    ]

    # 각 데이터셋을 데이터베이스에 추가합니다.
    for dataset_info in dataset_data:
        dataset = Dataset(name=dataset_info["name"], description=dataset_info["description"])
        db.session.add(dataset)
    
    db.session.commit()  # 변경사항을 커밋합니다.

# 함수 호출로 데이터셋 데이터 추가 실행
add_dataset_data()