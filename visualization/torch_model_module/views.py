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
from api_wrapper.api_wrapper import ModelAPI

from django.views.generic.edit import CreateView

class MainView(TemplateView):
    template_name = 'torch_model_module/models.html'

    def get(self,request):
        username = request.user.username
        private_models_list = TorchModel.objects.filter(username = username)
        public_models_list = TorchModel.objects.filter(username = 'public')
        context = {'private_models_list':private_models_list,'public_models_list':public_models_list}
        context.update({'nbar':'models','logged':True})
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


@login_required(login_url='/login/')
def upload_model(request):
    context = {'nbar':'models','logged':True}
    username = request.user.username
    if request.method == "POST":
        form = TorchModelForm(request.POST, request.FILES)
        if form.is_valid():
            obj = TorchModel() 
            obj.port = form.cleaned_data['port']
            obj.endpoint = form.cleaned_data['endpoint']
            obj.name = form.cleaned_data['name']
            obj.problem_type = form.cleaned_data['problem_type']
            obj.is_public = form.cleaned_data['is_public']
            if obj.is_public:
                obj.username = 'public'
            else:
                obj.username = username
            obj.save()
            #return detail(request, obj.id)
            return HttpResponseRedirect(f'/torch_models/{obj.id}/')
    else:
        form = TorchModelForm()

    context.update({'form':form})
    return render(request, 'torch_model_module/upload_model.html',context)

@login_required(login_url='/login/')
def detail(request, ex_id):
    context = {'nbar':'models','logged':True}

    if request.method == 'GET':

        model = get_object_or_404(TorchModel, pk=ex_id)
        model_wrapper = ModelAPI(model.endpoint,model.port)
        encoding_dict = model_wrapper.encoding_dict()
        active = False
        n_classes = None
        if encoding_dict:
            active = True
            n_classes = len(encoding_dict)

        context.update({'model': model, 'active':active,'encoding_dict':encoding_dict,'n_classes':n_classes})

    if request.method == 'POST':
        if 'delete' in request.POST:
            TorchModel.objects.filter(id=ex_id).delete()
            return redirect('/torch_models/')
        if 'back' in request.POST:
            return redirect('/torch_models/')

    
    return render(request, 'torch_model_module/detail.html', context)


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
