from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ImageModel
import sys
sys.path.append("..")
from uploader.models import Doc

# Create your views here.
def explorer(request):
    image_list = Doc.objects.all()
    len_image_list = len(image_list)

    #print(image_list)
    for img in image_list:
        print(img.image_url)
    return render(request, 'explorer/explorer.html',
    {'len_image_list':len_image_list,
    'image_list':image_list
    })