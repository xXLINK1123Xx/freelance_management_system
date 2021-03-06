from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic import DetailView
from api.models import *
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url="/login")
def home(request):
    return render(request, "web/projects.html")

def signup(request):
    return render(request, "registration/registration.html")

@login_required(login_url="/login")
def portfolio(request):
    if not request.user.is_superuser:
        u_role = request.user.profile.role
        if u_role == Profile.RoleValues.developer:
            try:
                return render(request, "web/portfolio.html", {'portfolio': Portfolio.objects.get(user=request.user)})
            except Portfolio.DoesNotExist:
                return render(request, "web/portfolio.html", {'portfolio': None})
        else:
            raise Http404("No portfolio is available for users who are %s" % u_role)
    else:
        raise Http404("No portfolio is available for superusers")

class AllProjectsListView(ListView):
    model = Project
    template_name = "web/projects.html"
    paginate_by = 10
    def get_queryset(self):
        return Project.objects.filter(stage=Project.StageValues.preparation)

class MyProjectsListView(LoginRequiredMixin, ListView):
    template_name = "web/projects.html"
    paginate_by = 10
    def get_queryset(self):
        if not self.request.user.is_superuser:
            if self.request.user.profile.role == Profile.RoleValues.creator:
                return Project.objects.filter(creator=self.request.user)
            elif self.request.user.profile.role == Profile.RoleValues.developer:
                return Project.objects.filter(applications__user=self.request.user).filter(applications__status__exact=Application.StatusValues.accepted)
        else:
            raise Http404("No projects are available for superuser")

class MyApplicationsListView(LoginRequiredMixin, ListView):
    template_name = "web/myapplications.html"
    paginate_by = 10
    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

class MyTasksListView(LoginRequiredMixin, ListView):
    template_name = "web/mytasks.html"
    paginate_by = 10
    def get_queryset(self):
        if not self.request.user.is_superuser:
            return Task.objects.filter(developers=self.request.user)
        else:
            raise Http404("No tasks are available for superuser")

class ProjectDetailView(LoginRequiredMixin, DetailView):
    template_name = "web/project.html"
    queryset = Project.objects.all()
    def get_object(self):
        obj = super(ProjectDetailView, self).get_object()
        print(obj)
        if obj.stage == Project.StageValues.preparation:
            print("Preparation case;")
            return obj
        elif obj.creator == self.request.user:
            print("Current user is owner;")
            return obj
        elif obj.stage == Project.StageValues.development:
            print("Development case;")
            if self.request.user in User.objects.filter(application__project=obj).filter(application__status__exact=Application.StatusValues.accepted):
                print("Current user is one of the developers;")
                return obj
            else:
                print("Current user is not one of the developers;")
                raise Http404("")
    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['team'] = User.objects.filter(application__project=Project.objects.filter(id=self.kwargs['pk'])).filter(application__status=Application.StatusValues.accepted)
        return context