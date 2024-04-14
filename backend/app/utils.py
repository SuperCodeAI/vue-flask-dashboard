import requests
from app import db
from app.models import Node

def fetch_and_store_node_data():
    try:
        response = requests.get('http://13.124.158.135:20001/api/v1/metrics')
        node_data_dict = response.json()

        for node_name, node_info in node_data_dict.items():
            # 존재하고 있는 노드인지 검색.
            existing_node = Node.query.filter_by(name=node_name).first()
            if existing_node:
                # 노드가 이미 존재하면 상태만 업데이트
                existing_node.status = 0  # 대기 상태로 업데이트
                existing_node.cpu_core_count = int(node_info['metrics'][0])
                existing_node.total_memory_mb = int(float(node_info['metrics'][9]) / (1024**2))
                existing_node.total_disk_mb = int(float(node_info['metrics'][10]) / (1024**2))
                existing_node.instance = node_info['instance'][0]
                existing_node.gpu_info = node_info['metrics'][11] if node_info['metrics'][11] else "None"
            else:
                # 존재하지 않는 노드라면 새로 추가
                metrics = node_info['metrics']
                cpu_core_count = int(metrics[0])
                total_memory_mb = int(float(metrics[9]) / (1024**2))
                total_disk_mb = int(float(metrics[10]) / (1024**2))
                instance_info = node_info['instance'][0]
                gpu_info = metrics[11] if metrics[11] else "None"

                node = Node(
                    name=node_name,
                    cpu_core_count=cpu_core_count,
                    total_memory_mb=total_memory_mb,
                    total_disk_mb=total_disk_mb,
                    status=0,  # 대기 : 0, 학습 중 : 1, 학습 완료: 2
                    instance=instance_info,
                    gpu_info=gpu_info
                )
                db.session.add(node)
        
        db.session.commit()
    except Exception as e:
        print(f"Error fetching or storing node data: {e}")
        