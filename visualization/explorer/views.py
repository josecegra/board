from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ImageModel
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required

import sys
sys.path.append("..")
from uploader.models import Doc

# Create your views here.
@login_required(login_url='/login/')
def explorer(request):


    
    if request.method == 'POST':
        if 'clear' in request.POST:
            image_list = Doc.objects.all()
            for img in image_list:
                img.delete()


    image_list = Doc.objects.all()
    len_image_list = len(image_list)

    return render(request, 'explorer/explorer.html',
    {'len_image_list':len_image_list,
    'image_list':image_list
    })

@login_required(login_url='/login/')
def detail(request, img_id):
    
    img = get_object_or_404(Doc, pk=img_id)
    context = {'img': img}

    if request.method == 'POST':
        if 'XAI' in request.POST:
            message = 'XAI should happen'
            context.update({'message':message})
            return render(request, 'explorer/detail.html', context)
        elif 'refresh' in request.POST:
            context = {'img': img}
            return render(request, 'explorer/detail.html', context)
        elif 'board' in request.POST:
            return redirect('/explorer')
        elif 'delete' in request.POST:
            Doc.objects.filter(id=img_id).delete()
            return redirect('/explorer')
    
    return render(request, 'explorer/detail.html', context)
