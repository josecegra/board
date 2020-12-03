from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from django.views.generic import TemplateView
from .models import DatasetModel
from .forms import DatasetForm
# Create your views here.
class DatasetsMainView(TemplateView):
    template_name = 'datasets/datasets.html'

    def get(self,request):
        username = request.user.username
        #private models 
        private_dataset_list = DatasetModel.objects.filter(username = username)
        #public models
        public_dataset_list = DatasetModel.objects.filter(username = 'public')
        #print(len(models_list))
        context = {'private_dataset_list':private_dataset_list,'public_dataset_list':public_dataset_list}
        return render(request, self.template_name,context)


def create_dataset(request):
    username = request.user.username
    if request.method == "POST":
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            obj = DatasetModel() 
            #obj.upload = form.cleaned_data['upload']
            obj.name = form.cleaned_data['name']
            obj.problem_type = form.cleaned_data['problem_type']
            obj.is_public = form.cleaned_data['is_public']
            if obj.is_public:
                obj.username = 'public'
            else:
                obj.username = username
            obj.save()
            return HttpResponseRedirect('/datasets/')
    else:
        form = DatasetForm()
    context = {'form':form}
    return render(request, 'datasets/create_dataset.html',context)


def detail(request, ex_id):
    
    img = get_object_or_404(DatasetModel, pk=ex_id)
    context = {'img': img}

    # if request.method == 'POST':
    #     if 'XAI' in request.POST:
    #         message = 'XAI should happen'
    #         context.update({'message':message})
    #         return render(request, 'e/detail.html', context)
    #     elif 'refresh' in request.POST:
    #         context = {'img': img}
    #         return render(request, 'board/detail.html', context)
    #     elif 'board' in request.POST:
    #         return redirect('/board')
    #     elif 'delete' in request.POST:
    #         ImageModel.objects.filter(id=img_id).delete()
    #         return redirect('/board')
    
    return render(request, 'datasets/detail.html', context)