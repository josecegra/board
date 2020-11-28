from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage

# Create your views here.
from .models import Doc
def uploader(request):
    return HttpResponse('<p>H<p/>')

class MainView(TemplateView):
    template_name = 'uploader/uploader.html'

def file_upload_view(request):
    print(request.FILES)
    if request.method == 'POST':
        myfile = request.FILES.get('file')

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        #fs = FileSystemStorage()
        #print(dir(my_file))
        #print(my_file.name)
        #uploaded_file_url = 'media/'+my_file.name
        #uploaded_file_url = fs.url(my_file.name)

        Doc.objects.create(upload = myfile, image_url = uploaded_file_url)
        return HttpResponse('')
    return JsonResponse({'post':'false'})
