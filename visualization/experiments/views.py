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


def detail(request, ex_id):
    experiment = get_object_or_404(ExperimentModel, pk=ex_id)
    if experiment:
        img_list = experiment.dataset.img_list.all()

    context = {'experiment': experiment,'img_list':img_list}
    if request.method == 'POST':
        if 'delete' in request.POST:
            ExperimentModel.objects.filter(id=ex_id).delete()
            return redirect('/experiments/')

    return render(request, 'experiments/detail.html', context)
