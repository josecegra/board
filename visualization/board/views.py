from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from django.http import HttpResponse
from .models import ImageModel
from .forms import ButtonForm
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def index(request):

    image_list = ImageModel.objects.all()
    len_image_list = len(image_list)
    if request.method == 'POST' and request.FILES[str(len_image_list)]:
        myfile = request.FILES[str(len_image_list)]
        #print(type(myfile))
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        img_object = ImageModel(name = filename,image_url=uploaded_file_url)
        img_object.save()
        return render(request, 'board/index.html', {
            'uploaded_file_url': uploaded_file_url,
            'len_image_list':len_image_list
        })
    return render(request, 'board/index.html',
    {'len_image_list':len_image_list,
    'image_list':image_list
    })


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'board/index.html', context)


# https://docs.djangoproject.com/en/3.1/topics/forms/

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
    
    return render(request, 'board/detail.html', context)



    

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))