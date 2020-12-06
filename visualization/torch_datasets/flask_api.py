import io
import json
import numpy as np
import torch.nn as nn

import torch
import torchvision
from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request

import sys
sys.path.append('../')

class ResNet(nn.Module):
    def __init__(self,size, output_size):
        super(ResNet, self).__init__()

        if size not in [18,34,50,101,152]:
            raise Exception('Wrong size for resnet')
        if size == 18:
            self.net = torchvision.models.resnet18(pretrained=True)
        elif size == 34:
            self.net = torchvision.models.resnet34(pretrained=True)
        elif size == 50:
            self.net = torchvision.models.resnet50(pretrained=True)
        elif size == 101:
            self.net = torchvision.models.resnet101(pretrained=True)
        elif size == 152:
            self.net = torchvision.models.resnet152(pretrained=True)

        #initialize the fully connected layer
        self.net.fc = nn.Linear(self.net.fc.in_features, output_size)
        self.sm = nn.Softmax(dim=1)

    def forward(self, x):
        out = self.net(x)
        out = self.sm(out)
        return out


def transform_image(image_bytes):
    base_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        # this normalization is required https://pytorch.org/tutorials/beginner/finetuning_torchvision_models_tutorial.html
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')    
    image = base_transform(image)
    return image.unsqueeze(0)

def get_prediction(model,image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = y_hat.item()
    return str(predicted_idx), class_index_dict[predicted_idx]

def load_model(model_name,model_path,class_index_dict):
    output_size = len(class_index_dict)
    if model_name.startswith("resnet"):
        size = int(model_name.replace("resnet",""))
        model = ResNet(size,output_size)
    model = nn.DataParallel(model)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def define_app(model):
    app = Flask(__name__)
    @app.route('/sortifier', methods=['POST'])
    def predict(model):
        if request.method == 'POST':
            file = request.files['file']
            img_bytes = file.read()
            class_id, class_name = get_prediction(model,image_bytes=img_bytes)
            return jsonify({'class_id': class_id, 'class_name': class_name})

    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        shutdown_server()
        return 'Server shutting down...'

    return app


if __name__=="__main__":
    
    class_index_dict = {0:'bitewings',1:'cephalometrics',2:'panoramics',3:'periapicals'}
    model_path = 'torch_datasets/model_checkpoint.pth'
    model_name = 'resnet34'

    model = load_model(model_name,model_path,class_index_dict)
    app = define_app(model)
    app.run(host='localhost', port=5000)
    #print(dir(app))
    #print(app.url_map)

