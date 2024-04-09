from app import db
from app.models import Node

def drop_node_table():
    # SQLAlchemy 메타데이터 객체를 사용하여 Node 테이블만을 대상으로 drop 작업을 수행
    Node.__table__.drop(db.engine)

    # 변경사항을 데이터베이스에 적용
    db.session.commit()