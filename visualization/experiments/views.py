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
from django.contrib.auth.decorators import login_required


from api_wrapper.api_wrapper import ModelAPI
#from torch_datasets.flask_api import *



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
        context.update({'nbar':'experiments','logged':True})
        return render(request, self.template_name,context)

@login_required(login_url='/login/')
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
            #print(form.cleaned_data['torch_model'].endpoint)
            #obj.torch_model.create(name = 'test')
            #print(dir(torch_model))
            #print(torch_model.values)
            #torch_model.save()
            #obj.torch_model.set(torch_model)
            #obj.dataset.set(form.cleaned_data['dataset'])
            if obj.is_public:
                obj.username = 'public'
            else:
                obj.username = username
            obj.save()
            return HttpResponseRedirect(f'/experiments/{obj.id}')
    else:
        form = ExperimentForm()
    context = {'form':form}
    context.update({'nbar':'experiments','logged':True})
    return render(request, 'experiments/create_experiment.html',context)

@login_required(login_url='/login/')
def detail_experiment(request, ex_id):
    experiment = get_object_or_404(ExperimentModel, pk=ex_id)
    #print(experiment.dataset.all())
    #dataset_id = experiment.dataset.pk

    #dataset_list = list(experiment.dataset.all())
    #print(len(dataset_list))
    
    if experiment:
        img_list = experiment.dataset.img_list.all()
        #img_list = []

    #torch_model = TorchModel.objects.filter(id = experiment.torch_model.id)
    torch_model = None
    context = {'experiment': experiment,'img_list':img_list,'active_models':torch_model}
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('/experiments/')
        if 'delete' in request.POST:
            ExperimentModel.objects.filter(id=ex_id).delete()
            return redirect('/experiments/')

        
        torch_model = TorchModel.objects.filter(id = experiment.torch_model.id)
        context.update({'active_models':torch_model})

    context.update({'nbar':'experiments','logged':True})
    return render(request, 'experiments/detail_experiment.html', context)


@login_required(login_url='/login/')
def detail_image(request, ex_id,img_id):
    img = get_object_or_404(ImageModel, pk=img_id)
    experiment = get_object_or_404(ExperimentModel, pk=ex_id)
    context = {'img': img,'experiment':experiment,'nbar':'experiments','logged':True}
    if request.method == 'GET':
        return render(request, 'experiments/detail_image.html', context)
    
    if request.method == 'POST':

        if 'board' in request.POST:
            return redirect(f'/experiments/{ex_id}')
        if 'delete' in request.POST:
            ImageModel.objects.filter(id=img_id).delete()
            return redirect(f'/experiments/{ex_id}')

        if 'predict' in request.POST:
            torch_model = get_object_or_404(TorchModel, pk=experiment.torch_model.id)
            img = get_object_or_404(ImageModel, pk=img_id)
            img_path = img.img_file.path

            model_wrapper = ModelAPI(torch_model.endpoint,torch_model.port)
            pred_dict = model_wrapper.predict(img_path)
            for k in pred_dict.keys():
                pred = pred_dict[k]
            XAI_path = pred['XAI_path']
            #move to static
            dest_path = MEDIA_ROOT
            fname = "XAI_"+os.path.split(XAI_path)[1]
            dest_file_path = os.path.join(dest_path,fname)
            copyfile(XAI_path,dest_file_path)

            fs = FileSystemStorage()
            myfile = fs.open(dest_file_path)  
            uploaded_file_url = fs.url(dest_file_path)   
            XAI_img = ImageModel(filename = fname, img_file = myfile, img_url = uploaded_file_url) 

            context.update({'class':pred['class'],'XAI_img':XAI_img})

            context.update({'message':dest_file_path})
            return render(request, 'experiments/detail_image.html', context)
        if 'XAI' in request.POST:
            message = 'XAI should happen'
            context.update({'message':message})
            return render(request, 'experiments/detail_image.html', context)
        if 'refresh' in request.POST:
            return render(request, 'experiments/detail_image.html', context)


    
