import requests
from app import db
from app.models import Node

def fetch_and_store_node_data():
    try:
        response = requests.get('http://163.180.117.47:20001/api/v1/metrics')
        node_data_dict = response.json()

        for node_name, node_info in node_data_dict.items():
            # 메트릭 데이터 추출
            metrics = node_info['metrics']
            cpu_count = int(metrics[0])
            # 메모리와 디스크를 GB 단위로 변환하고 소수점 셋째 자리에서 반올림
            total_memory_gb = round(float(metrics[9]) / (1024**3), 2)
            total_disk_gb = round(float(metrics[10]) / (1024**3), 2)

            # Node 객체 생성 및 데이터베이스에 추가
            node = Node(
                name=node_name,
                cpu_count=cpu_count,
                total_memory=total_memory_gb,
                total_disk=total_disk_gb,
                status=0  # 대기 : 0 , 학습 중 : 1, 학습 완료: 2
            )
            db.session.add(node)
        
        db.session.commit()
    except Exception as e:
        print(f"Error fetching or storing node data: {e}")