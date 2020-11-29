import os
import sys

from shutil import copyfile
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.core.files import File  # you need this somewhere
from django.conf import settings
# Create your views here.
from .models import Doc

class MainView(TemplateView):
    template_name = 'uploader/uploader.html'
    def post(self,request):
        fs = FileSystemStorage()
        print(settings.BASE_DIR)

        media_dir = os.path.join(settings.BASE_DIR,'media')
        path = request.POST.get('path')
        for filename in os.listdir(path):
            
            src_file_path = os.path.join(path,filename)
            dest_file_path = os.path.join(media_dir,filename)
            copyfile(src_file_path,dest_file_path)

            myfile = fs.open(dest_file_path)  
            uploaded_file_url = fs.url(dest_file_path)          
            Doc.objects.create(upload = myfile, image_url = uploaded_file_url)

        context = {}
        return render(request, self.template_name,context)


def file_upload_view(request):
    print(request.FILES)
    if request.method == 'POST':
        myfile = request.FILES.get('file')
        print(type(myfile))
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(filename)
        print(uploaded_file_url)
        #fs = FileSystemStorage()
        #print(dir(my_file))
        #print(my_file.name)
        #uploaded_file_url = 'media/'+my_file.name
        #uploaded_file_url = fs.url(my_file.name)

        Doc.objects.create(upload = myfile, image_url = uploaded_file_url)
        return HttpResponse('')
    return JsonResponse({'post':'false'})
