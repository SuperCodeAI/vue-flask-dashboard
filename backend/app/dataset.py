from app.extensions import db
from app.models import Dataset

def add_dataset_data():
    # Define the model data to be added
    dataset_data = [
        {
            "name": "MNIST",
            "description": "MNIST 데이터셋은 손으로 쓴 숫자들의 대규모 데이터베이스로, 0부터 9까지의 숫자 이미지로 구성되어 있습니다. 각 이미지는 28x28 픽셀의 그레이스케일 이미지입니다. 주로 이미지 처리 시스템을 훈련시키고 테스트하는 데 사용되며, 기계 학습 분야에서 가장 기본적인 데이터셋 중 하나로 평가받습니다."
        },
        {
            "name": "pandas-datareader(주식 데이터)",
            "description": "pandas-datareader는 다양한 금융 데이터 소스로부터 데이터를 읽어오는 파이썬 라이브러리입니다. 이를 통해 사용자는 주식, 채권, 기타 금융 관련 데이터를 쉽게 가져올 수 있습니다. 해당 데이터셋은 주식 데이터를 가져왔습니다." },
    ]

    # 각 데이터셋을 데이터베이스에 추가합니다.
    for dataset_info in dataset_data:
        dataset = Dataset(name=dataset_info["name"], description=dataset_info["description"])
        db.session.add(dataset)
    
    db.session.commit()  # 변경사항을 커밋합니다.

# 함수 호출로 데이터셋 데이터 추가 실행
add_dataset_data()