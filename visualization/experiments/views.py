from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from django.views.generic import TemplateView
from .models import ExperimentModel
from .forms import ExperimentForm
from django.core.files.storage import FileSystemStorage

import os
from shutil import copyfile
from django.core.files import File
from visualization.settings import MEDIA_ROOT
from datasets.models import ImageModel
from torch_model_module.models import TorchModel


from torch_datasets.flask_api import *

def Sortifier(img_path_list):
    import requests
    url = "http://localhost:5000/sortifier"

    if isinstance(img_path_list,str):
        img_path_list = [img_path_list]

    pred_dict = {}
    for img_path in img_path_list:
        #try:
        resp = requests.post(url, files={"file": open(img_path,'rb')}).json() 
        print(resp)    
        pred_dict.update({img_path:resp['class_name']})
        #except:
        #print(f'Something went wrong when predicting {img_path}') 

    return pred_dict

def get_images(images_path):
    dest_path = MEDIA_ROOT
    fs = FileSystemStorage()
    img_list = []
    for fname in os.listdir(images_path):
        fpath = os.path.join(images_path,fname)
        dest_file_path = os.path.join(dest_path,fname)
        copyfile(fpath,dest_file_path)
        myfile = fs.open(dest_file_path)  
        uploaded_file_url = fs.url(dest_file_path)   
        obj = ImageModel(filename = fname, img_file = myfile, img_url = uploaded_file_url) 
        obj.save()
        img_list.append(obj)
    
    return img_list

class ExperimentsMainView(TemplateView):
    template_name = 'experiments/experiments.html'

    def get(self,request):
        username = request.user.username
        private_experiment_list = ExperimentModel.objects.filter(username = username)
        public_experiment_list = ExperimentModel.objects.filter(username = 'public')
        context = {'private_experiment_list':private_experiment_list,'public_experiment_list':public_experiment_list}
        return render(request, self.template_name,context)


def create_experiment(request):
    username = request.user.username
    if request.method == "POST":
        form = ExperimentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = ExperimentModel() 
            obj.name = form.cleaned_data['name']
            obj.is_public = form.cleaned_data['is_public']
            obj.torch_model = form.cleaned_data['torch_model']
            obj.dataset = form.cleaned_data['dataset']
            if obj.is_public:
                obj.username = 'public'
            else:
                obj.username = username
            obj.save()
            return HttpResponseRedirect(f'/experiments/{obj.id}')
    else:
        form = ExperimentForm()
    context = {'form':form}
    return render(request, 'experiments/create_experiment.html',context)


def detail_experiment(request, ex_id):
    experiment = get_object_or_404(ExperimentModel, pk=ex_id)
    if experiment:
        img_list = experiment.dataset.img_list.all()

    active_models = TorchModel.objects.filter(active = True)

    context = {'experiment': experiment,'img_list':img_list,'active_models':active_models}
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('/experiments/')
        if 'delete' in request.POST:
            ExperimentModel.objects.filter(id=ex_id).delete()
            return redirect('/experiments/')
        if 'activate' in request.POST:
            #create api
            torch_model = experiment.torch_model
            model_name = torch_model.name
            if torch_model.active == False:
                torch_model.active = True
                torch_model.save()
                context.update({'message':f'model {model_name} activated'})
            else:
                context.update({'message':f'model {model_name} already active'})

        for model in active_models:
            if f'deactivate_{model.id}' in request.POST:
                model.active = False
                model.save()
                context.update({'message':f'model {model.name} deactivated'})

        
        active_models = TorchModel.objects.filter(active = True)
        context.update({'active_models':active_models})

 
    return render(request, 'experiments/detail_experiment.html', context)


def detail_image(request, ex_id,img_id):
    img = get_object_or_404(ImageModel, pk=img_id)
    experiment = get_object_or_404(ExperimentModel, pk=ex_id)
    
    context = {'img': img,'experiment':experiment}
    if request.method == 'POST':
        if 'predict' in request.POST:
            class_index_dict = {0:'bitewings',1:'cephalometrics',2:'panoramics',3:'periapicals'}
            model_path = 'torch_datasets/model_checkpoint.pth'
            model_name = 'resnet34'

            #model = load_model(model_name,model_path,class_index_dict)
            #app = define_app(model)
            import subprocess
            from subprocess import call, run
            run(["python", "torch_datasets/flask_api.py"], stdout=subprocess.DEVNULL)
            print('flask app running')
            prediction_dict = Sortifier('torch_datasets/tmp.jpg')
            
            #app.run(host='localhost', port=5050,debug=True,use_reloader=False)
            
            message = f'{prediction_dict}'
            context.update({'message':message})
            return render(request, 'experiments/detail_image.html', context)
        if 'XAI' in request.POST:
            message = 'XAI should happen'
            context.update({'message':message})
            return render(request, 'experiments/detail_image.html', context)
        if 'refresh' in request.POST:
            context = {'img': img}
            return render(request, 'experiments/detail_image.html', context)
        if 'board' in request.POST:
            return redirect(f'/experiments/{ex_id}')
        if 'delete' in request.POST:
            ImageModel.objects.filter(id=img_id).delete()
            return redirect(f'/experiments/{ex_id}')
    
    return render(request, 'experiments/detail_image.html', context)
