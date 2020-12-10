import io
import json
import numpy as np
import torch.nn as nn
import os

import torch
import torchvision
from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request

import matplotlib.pyplot as plt

import sys
sys.path.append('../')

from gradcam import grad_cam


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

def get_transform():
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        # this normalization is required https://pytorch.org/tutorials/beginner/finetuning_torchvision_models_tutorial.html
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

def transform_image(image_bytes):
    base_transform = get_transform()
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')    
    image = base_transform(image)
    return image.unsqueeze(0)

def get_prediction(model,image_bytes,filename):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = y_hat.item()

    #XAI
    heatmap_layer = model.module.net.layer4[2].conv2
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB') 
    image_interpretable = grad_cam(model, image, heatmap_layer, get_transform())

    print(type(image_interpretable))



    # fig,ax = plt.subplots()
    # ax.imshow(image_interpretable)
    # ax.axis('off')

    images_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'images')
    if not os.path.exists(images_path):
        os.mkdir(images_path)
    XAI_path = os.path.join(images_path,filename)
    # fig.tight_layout()

    # fig.savefig(XAI_path, bbox_inches='tight')

    XAI_img = Image.fromarray(image_interpretable).convert('RGB')
    XAI_img.save(XAI_path)

    return str(predicted_idx), class_index_dict[predicted_idx], XAI_path

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

def define_app(model,endpoint_name,class_index_dict):
    app = Flask(__name__)
    @app.route(f'/{endpoint_name}', methods=['POST','GET'])
    def predict():
        if request.method == 'POST':
            file = request.files['file']
            img_bytes = file.read()            
            class_id, class_name, XAI_path = get_prediction(model,img_bytes,file.filename)
            return jsonify({'class_id': class_id, 'class_name': class_name,'XAI_path': XAI_path})
        if request.method == 'GET':
            return jsonify({'encoding_dict': class_index_dict})


    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        shutdown_server()
        return 'Server shutting down...'

    return app


if __name__=="__main__":
    
    class_index_dict = {0:'bitewings',1:'cephalometrics',2:'panoramics',3:'periapicals'}
    model_path = 'model_checkpoint.pth'
    model_name = 'resnet34'
    model = load_model(model_name,model_path,class_index_dict)


    endpoint_name = 'sortifier'
    app = define_app(model,endpoint_name,class_index_dict)
    app.run(host='localhost', port=5000)


