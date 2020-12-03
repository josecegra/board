from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from django.views.generic import TemplateView
from .models import ExperimentModel
from .forms import ExperimentForm
# Create your views here.
class ExperimentsMainView(TemplateView):
    template_name = 'experiments/experiments.html'

    def get(self,request):
        username = request.user.username
        private_experiment_list = ExperimentModel.objects.filter(username = username)
        public_experiment_list = ExperimentModel.objects.filter(username = 'public')
        #print(len(models_list))
        context = {'private_experiment_list':private_experiment_list,'public_experiment_list':public_experiment_list}
        return render(request, self.template_name,context)


def create_experiment(request):
    username = request.user.username
    if request.method == "POST":
        form = ExperimentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = ExperimentModel() 
            #obj.upload = form.cleaned_data['upload']
            obj.name = form.cleaned_data['name']
            #obj.problem_type = form.cleaned_data['problem_type']
            obj.is_public = form.cleaned_data['is_public']
            if obj.is_public:
                obj.username = 'public'
            else:
                obj.username = username
            obj.save()
            return HttpResponseRedirect('/experiments/')
    else:
        form = ExperimentForm()
    context = {'form':form}
    return render(request, 'experiments/create_experiment.html',context)