import os
import sys

from shutil import copyfile
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.core.files import File  # you need this somewhere
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import TorchModel
from .forms import TorchModelForm

from django.views.generic.edit import CreateView

class MainView(TemplateView):
    template_name = 'torch_model_module/models.html'

    def get(self,request):
        username = request.user.username
        print(username)
        #private models 
        private_models_list = TorchModel.objects.filter(username = username)
        #public models
        public_models_list = TorchModel.objects.filter(username = 'public')
        #print(len(models_list))
        context = {'private_models_list':private_models_list,'public_models_list':public_models_list}
        return render(request, self.template_name,context)
        
    
    def post(self,request):
        
        username = request.user.username
        fs = FileSystemStorage()
        media_dir = os.path.join(settings.BASE_DIR,'media')
        path = request.POST.get('path')
        if path:
            for i,filename in enumerate(os.listdir(path)):
                
                src_file_path = os.path.join(path,filename)
                dest_file_path = os.path.join(media_dir,filename)
                copyfile(src_file_path,dest_file_path)

                myfile = fs.open(dest_file_path)  
                uploaded_file_url = fs.url(dest_file_path)          
                TorchModel.objects.create(upload = myfile, weights_url = uploaded_file_url, user=username)
            message = f'Added {i} images'
        else:
            message = 'Empty path entered'
        context = {'message':message}
        return render(request, self.template_name,context)


class TorchModelView(CreateView):
    template_name = 'torch_model_module/upload_model.html'
    model = TorchModel
    fields = ['name', 'upload']


def upload_model(request):
    username = request.user.username
    if request.method == "POST":
        form = TorchModelForm(request.POST, request.FILES)
        if form.is_valid():
            obj = TorchModel() 
            obj.upload = form.cleaned_data['upload']
            obj.name = form.cleaned_data['name']
            obj.problem_type = form.cleaned_data['problem_type']
            obj.is_public = form.cleaned_data['is_public']
            if obj.is_public:
                obj.username = 'public'
            else:
                obj.username = username
            obj.save()
            return HttpResponseRedirect('/torch_models/')
    else:
        form = TorchModelForm()
    context = {'form':form}
    return render(request, 'torch_model_module/upload_model.html',context)

def detail(request, ex_id):
    experiment = get_object_or_404(TorchModel, pk=ex_id)
    context = {'experiment': experiment}
    if request.method == 'POST':
        if 'delete' in request.POST:
            TorchModel.objects.filter(id=ex_id).delete()
            return redirect('/torch_models/')

    return render(request, 'torch_model_module/detail.html', context)

    # def get(self,request):
    #     #username = request.user.username
    #     #models_list = TorchModel.objects.filter(user = username)
    #     #print(len(models_list))
    #     form = TorchModelForm()
    #     context = {'form':form}
    #     return render(request, self.template_name,context)

    # def post(self,request):
    #     username = request.user.username

    #     form = TorchModelForm(request.POST)
    #     # check whether it's valid:
    #     if form.is_valid():
    #         return HttpResponseRedirect('torch_models/')
            
    #     # uploaded_file_url = fs.url(filename)
    #     #TorchModel.objects.create(upload = myfile, weights_url = uploaded_file_url,user = username)


    #     context = {'form': form}
    #     return render(request, self.template_name,context)



@login_required(login_url='/login/')
def file_upload_view(request):
    username = request.user.username
    if request.method == 'POST':
        myfile = request.FILES.get('file')
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        TorchModel.objects.create(upload = myfile, weights_url = uploaded_file_url,user = username)
        return HttpResponse('')

    return JsonResponse({'post':'false'})
