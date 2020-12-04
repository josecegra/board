from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from .models import DatasetModel, ImageModel
from .forms import DatasetForm
from django.core.files.storage import FileSystemStorage

import os
from shutil import copyfile

from django.core.files import File

def get_images(images_path):
    dest_path = 'C:/Users/Jose Eduardo/Desktop/projects/web_dev/board/visualization/media'
    
    fs = FileSystemStorage()
    img_list = []
    for fname in os.listdir(images_path):
        fpath = os.path.join(images_path,fname)
        dest_file_path = os.path.join(dest_path,fname)
        copyfile(fpath,dest_file_path)
        
        myfile = fs.open(dest_file_path)  
        uploaded_file_url = fs.url(dest_file_path)   
        #djangofile = File(open(dest_file_path,'r',encoding="utf8"))
        obj = ImageModel() 
        obj.filename = fname
        obj.img_file = myfile
        obj.img_url = uploaded_file_url
        obj.save()
        img_list.append(obj)
    
    return img_list



class DatasetsMainView(TemplateView):
    template_name = 'datasets/datasets.html'
    def get(self,request):
        username = request.user.username
        private_dataset_list = DatasetModel.objects.filter(username = username)
        public_dataset_list = DatasetModel.objects.filter(username = 'public')
        context = {'private_dataset_list':private_dataset_list,'public_dataset_list':public_dataset_list}
        return render(request, self.template_name,context)

def create_dataset(request):
    username = request.user.username
    if request.method == "POST":
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():

            images_path = form.cleaned_data['images_path']
            img_list = []
            if images_path and os.path.exists(images_path):
                img_list = get_images(images_path)


            #print(len(img_list))
            obj = DatasetModel() 
            obj.name = form.cleaned_data['name']
            obj.problem_type = form.cleaned_data['problem_type']
            obj.images_path = form.cleaned_data['images_path']
            obj.annotations_path = form.cleaned_data['annotations_path']
            obj.annotations_upload = form.cleaned_data['annotations_upload']
            #obj.img_list = img_list

            if obj.is_public:
                obj.username = 'public'
            else:
                obj.username = username
            obj.save()

            for img in img_list:
                obj.img_list.add(img.id)
            return HttpResponseRedirect(f'/datasets/{obj.id}')
    else:
        form = DatasetForm()
    context = {'form':form}
    return render(request, 'datasets/create_dataset.html',context)

def detail(request, ex_id):
    import os
    dataset = get_object_or_404(DatasetModel, pk=ex_id)
    img_list = dataset.img_list
    img_list = img_list.all()

    #print(len(img_list))

    #print(dir(experiment))
    #message = os.listdir(dataset.images_path)
    message = ''
    context = {'experiment': dataset,'message':message,'img_list':img_list}
    if request.method == 'POST':
        if 'delete' in request.POST:
            DatasetModel.objects.filter(id=ex_id).delete()
            return redirect('/datasets/')

    return render(request, 'datasets/detail.html', context)


# get images when the path is set

    # def post(self,request):
    #     username = request.user.username
    #     fs = FileSystemStorage()
    #     media_dir = os.path.join(settings.BASE_DIR,'media')
    #     path = request.POST.get('path')
    #     if path:
    #         for i,filename in enumerate(os.listdir(path)):
                
    #             src_file_path = os.path.join(path,filename)
    #             dest_file_path = os.path.join(media_dir,filename)
    #             copyfile(src_file_path,dest_file_path)

    #             myfile = fs.open(dest_file_path)  
    #             uploaded_file_url = fs.url(dest_file_path)          
    #             Doc.objects.create(upload = myfile, image_url = uploaded_file_url, user=username)
    #         message = f'Added {i} images'
    #     else:
    #         message = 'Empty path entered'
    #     context = {'message':message}
    #     return render(request, self.template_name,context)