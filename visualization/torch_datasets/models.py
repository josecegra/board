import torch.nn as nn
import torchvision
import torch


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


def load_model(model_name,model_path,device,multi_gpu,output_size = None):
    net = build_model(model_name, device, multi_gpu, output_size=output_size, show=False)
    print(f'Loading model from {model_path}')
    net.load_state_dict(torch.load(model_path))
    print(f'Finished loading model {model_name}')
    return net

def build_model(model_name, device, multi_gpu, output_size=None, show=False):

    print(f'Building model {model_name}')
    # if model_name == "CNN":
    #     net = models.ConvNet(output_size)

    if model_name.startswith("resnet"):
        size = int(model_name.replace("resnet",""))
        #print(size,output_size)
        net = ResNet(size,output_size)
        #net = models.ResNetExperimental(size,output_size)

    #multiprocessing model
    if multi_gpu:
        net = nn.DataParallel(net)
    net = net.to(device)
    
    if show:
        print(net)

    return net
