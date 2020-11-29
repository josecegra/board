from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ImageModel
from django.shortcuts import render, redirect,get_object_or_404

import sys
sys.path.append("..")
from uploader.models import Doc

# Create your views here.
def explorer(request):
    image_list = Doc.objects.all()
    len_image_list = len(image_list)

    return render(request, 'explorer/explorer.html',
    {'len_image_list':len_image_list,
    'image_list':image_list
    })

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
