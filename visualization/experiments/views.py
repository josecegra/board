from django.shortcuts import render,get_object_or_404,redirect
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
        context = {'private_experiment_list':private_experiment_list,'public_experiment_list':public_experiment_list}
        return render(request, self.template_name,context)


def create_experiment(request):
    username = request.user.username
    if request.method == "POST":
        form = ExperimentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = ExperimentModel() 
            obj.name = form.cleaned_data['name']
            obj.is_public = form.cleaned_data['is_public']
            obj.torch_model = form.cleaned_data['torch_model']
            obj.dataset = form.cleaned_data['dataset']
            if obj.is_public:
                obj.username = 'public'
            else:
                obj.username = username
            obj.save()
            return HttpResponseRedirect(f'/experiments/{obj.id}')
    else:
        form = ExperimentForm()
    context = {'form':form}
    return render(request, 'experiments/create_experiment.html',context)


def detail(request, ex_id):
    experiment = get_object_or_404(ExperimentModel, pk=ex_id)
    context = {'experiment': experiment}
    if request.method == 'POST':
        if 'delete' in request.POST:
            ExperimentModel.objects.filter(id=ex_id).delete()
            return redirect('/experiments/')

    return render(request, 'experiments/detail.html', context)
