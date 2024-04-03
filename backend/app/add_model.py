from app.extensions import db
from app.models import Model

def add_model_data():
    # 모델 데이터 정의
    models_to_add = [
        {
            "name": "vision_transformer",
            "description": "The Vision Transformer (ViT) is an image classification model pretrained in ImageNet (ILSVRC-2012), ImageNet-21k, and JFT."
        },
        {
            "name": "gpt-3",
            "description": "GPT-3 is a Generative Pretrained Transformer or “GPT”-style autoregressive language model with 175 billion parameters. Researchers at OpenAI developed the model to help us understand how increasing the parameter count of language models can improve task-agnostic, few-shot performance. Once built, we found GPT-3 to be generally useful and thus created an API to safely offer its capabilities to the world, so others could explore them for commercial and scientific purposes."
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
