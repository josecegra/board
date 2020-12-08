from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from django.http import HttpResponse
from .models import ImageModel
from django.shortcuts import render, redirect,get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def home(request):
    context = {'user':request.user,'nbar':'home','logged':True}
    return render(request, 'board/home.html',context)


#not used
def index(request):

    image_list = ImageModel.objects.all()
    len_image_list = len(image_list)

    if request.method == 'POST':
        if 'upload_img' in request.POST:
            if request.FILES and request.FILES['img']:
                myfile = request.FILES['img']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                img_object = ImageModel(name = filename,image_url=uploaded_file_url)
                img_object.save()
                return render(request, 'board/child.html', {
                    'uploaded_file_url': uploaded_file_url,
                    'len_image_list':len_image_list,
                    'image_list':image_list
                })

        if 'path' in request.POST:
            return render(request, 'board/child.html',
                {'len_image_list':len_image_list,
                'image_list':image_list
                })


    return render(request, 'board/child.html',
    {'len_image_list':len_image_list,
    'image_list':image_list
    })
    
def explorer(request):
    image_list = ImageModel.objects.all()
    len_image_list = len(image_list)
    return render(request, 'board/child.html',
    {'len_image_list':len_image_list,
    'image_list':image_list
    })

def detail(request, img_id):
    
    img = get_object_or_404(ImageModel, pk=img_id)
    context = {'img': img}

    if request.method == 'POST':
        if 'XAI' in request.POST:
            message = 'XAI should happen'
            context.update({'message':message})
            return render(request, 'board/detail.html', context)
        elif 'refresh' in request.POST:
            context = {'img': img}
            return render(request, 'board/detail.html', context)
        elif 'board' in request.POST:
            return redirect('/board')
        elif 'delete' in request.POST:
            ImageModel.objects.filter(id=img_id).delete()
            return redirect('/board')
    
    return render(request, 'board/detail.html', context)
