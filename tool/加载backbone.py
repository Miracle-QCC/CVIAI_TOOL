import torch
"""
可以给自定义的模型加载预训练模型
"""
def load_model(model, checkpoint):
    model_CKPT = torch.load(checkpoint)
    model_dict = model.state_dict()
    pretrained_dict = model_CKPT
    # 将不在model中的参数过滤掉
    new_dict = {k:v for k,v in pretrained_dict.items() if k in model_dict.keys()}
    # new_dict.pop("classifier.weight")
    # new_dict.pop("classifier.bias")
    model_dict.update(new_dict)
    model.load_state_dict(model_dict)
    return model
