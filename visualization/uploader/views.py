import os
import sys

from shutil import copyfile
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.core.files import File  # you need this somewhere
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Doc


class MainView(TemplateView):
    template_name = 'uploader/uploader.html'
    
    def post(self,request):
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
                Doc.objects.create(upload = myfile, image_url = uploaded_file_url)
            message = f'Added {i} images'
        else:
            message = 'Empty path entered'
        context = {'message':message}
        return render(request, self.template_name,context)

@login_required(login_url='/login/')
def file_upload_view(request):
    if request.method == 'POST':
        myfile = request.FILES.get('file')
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        Doc.objects.create(upload = myfile, image_url = uploaded_file_url)
        return HttpResponse('')
    return JsonResponse({'post':'false'})
