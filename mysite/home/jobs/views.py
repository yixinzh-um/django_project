from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy,reverse
from .models import Job,Comment, Fav, Employer,Location
from .owner import OwnerListView,OwnerDetailView,OwnerCreateView,OwnerUpdateView,OwnerDeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateForm,CommentForm,EmployerForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.humanize.templatetags.humanize import naturaltime
from .utils import dump_queries
from django.db.models import Q

class JobListView(OwnerListView):
    model = Job
    template_name = "jobs/job_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            query = Q(title__contains=strval)
            query.add(Q(employer__name__contains=strval), Q.OR)
            query.add(Q(location__name__contains=strval), Q.OR)
            query.add(Q(description__contains=strval), Q.OR)
            job_list = Job.objects.filter(query).select_related().order_by('-updated_at')[:10] 
        else :
            job_list = Job.objects.all().order_by('-updated_at')[:10]
        employ_count =Employer.objects.all().count()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_jobs.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        # Augment the job_list
        for obj in job_list:
            obj.natural_updated = naturaltime(obj.updated_at)         
        ctx = {'job_list' : job_list, 'favorites': favorites,'employ_count':employ_count,'search':strval}
        dump_queries()
        return render(request, self.template_name, ctx)




class JobDetailView(OwnerDetailView):
    model = Job
    template_name = "jobs/job_detail.html"
    def get(self, request, pk) :
        x = Job.objects.get(id=pk)
        comments = Comment.objects.filter(job=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'job' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)




class JobCreateView(LoginRequiredMixin, View):
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('jobs:all')
    model=Job

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        job = form.save(commit=False)
        job.owner = self.request.user
        job.save()
        return redirect(self.success_url)


class JobUpdateView(LoginRequiredMixin, View):
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('jobs:all')

    def get(self, request, pk):
        job = get_object_or_404(Job, id=pk, owner=self.request.user)
        form = CreateForm(instance=job)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        job = get_object_or_404(Job, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=job)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        job = form.save(commit=False)
        job.save()

        return redirect(self.success_url)

class JobDeleteView(OwnerDeleteView):
    model = Job
    template_name = "jobs/job_confirm_delete.html"



class EmployerListView(OwnerListView):
    model = Employer
    template_name = "employers/employer_list.html"

    def get(self, request) :
        employer_list = Employer.objects.all()
        ctx = {'employer_list' : employer_list}
        return render(request, self.template_name, ctx)


class EmployerCreateView(LoginRequiredMixin, View):
    template_name = 'employers/employer_form.html'
    success_url = reverse_lazy('jobs:all')

    
    def get(self, request, pk=None):
        form = EmployerForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = EmployerForm(request.POST, request.FILES or None)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        employer = form.save(commit=False)
        employer.owner = self.request.user
        employer.save()
        return redirect(self.success_url)


class EmployerUpdateView(LoginRequiredMixin, View):
    template_name = 'employers/employer_form.html'
    success_url = reverse_lazy('jobs:all')

    def get(self, request, pk):
        employer = get_object_or_404(Employer, id=pk, owner=self.request.user)
        form = EmployerForm(instance=employer)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        employer = get_object_or_404(Employer, id=pk, owner=self.request.user)
        form = EmployerForm(request.POST, request.FILES or None, instance=employer)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        employer = form.save(commit=False)
        employer.save()

        return redirect(self.success_url)

class EmployerDeleteView(OwnerDeleteView):
    model = Employer
    template_name = "employers/employer_confirm_delete.html"
    success_url = reverse_lazy('jobs:all')




# class TitleListView(OwnerListView):
#     model = Title
#     template_name = "titles/title_list.html"

#     def get(self, request) :
#         title_list = Title.objects.all()
#         ctx = {'title_list' : title_list}
#         return render(request, self.template_name, ctx)


# class TitleCreateView(LoginRequiredMixin, View):
#     template_name = 'titles/title_form.html'
#     success_url = reverse_lazy('jobs:all')

    
#     def get(self, request, pk=None):
#         form = TitleForm()
#         ctx = {'form': form}
#         return render(request, self.template_name, ctx)

#     def post(self, request, pk=None):
#         form = TitleForm(request.POST, request.FILES or None)
#         if not form.is_valid():
#             ctx = {'form': form}
#             return render(request, self.template_name, ctx)

#         # Add owner to the model before saving
#         title = form.save(commit=False)
#         title.owner = self.request.user
#         title.save()
#         return redirect(self.success_url)


# class TitleUpdateView(LoginRequiredMixin, View):
#     template_name = 'titles/title_form.html'
#     success_url = reverse_lazy('jobs:all')

#     def get(self, request, pk):
#         title = get_object_or_404(Title, id=pk, owner=self.request.user)
#         form = TitleForm(instance=title)
#         ctx = {'form': form}
#         return render(request, self.template_name, ctx)

#     def post(self, request, pk=None):
#         title = get_object_or_404(Title, id=pk, owner=self.request.user)
#         form = TitleForm(request.POST, request.FILES or None, instance=title)

#         if not form.is_valid():
#             ctx = {'form': form}
#             return render(request, self.template_name, ctx)

#         title = form.save(commit=False)
#         title.save()

#         return redirect(self.success_url)

# class TitleDeleteView(OwnerDeleteView):
#     model = Title
#     template_name = "titles/title_confirm_delete.html"
#     success_url = reverse_lazy('jobs:all')


class LocationListView(OwnerListView):
    model = Location
    template_name = "locations/location_list.html"

    def get(self, request) :
        location_list = Location.objects.all()
        ctx = {'location_list' : location_list}
        return render(request, self.template_name, ctx)


class LocationCreateView(LoginRequiredMixin, View):
    template_name = 'locations/location_form.html'
    success_url = reverse_lazy('jobs:all')

    
    def get(self, request, pk=None):
        form = LocationForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = LocationForm(request.POST, request.FILES or None)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        location = form.save(commit=False)
        location.owner = self.request.user
        location.save()
        return redirect(self.success_url)


class LocationUpdateView(LoginRequiredMixin, View):
    template_name = 'locations/location_form.html'
    success_url = reverse_lazy('jobs:all')

    def get(self, request, pk):
        location = get_object_or_404(Location, id=pk, owner=self.request.user)
        form = LocationForm(instance=location)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        location = get_object_or_404(Location, id=pk, owner=self.request.user)
        form = LocationForm(request.POST, request.FILES or None, instance=location)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        location = form.save(commit=False)
        location.save()

        return redirect(self.success_url)

class LocationDeleteView(OwnerDeleteView):
    model = Location
    template_name = "locations/location_confirm_delete.html"
    success_url = reverse_lazy('jobs:all')


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Job, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, job=f)
        comment.save()
        return redirect(reverse('jobs:job_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "jobs/comment_delete.html"




# def stream_file(request, pk):
#     job = get_object_or_404(Job, id=pk)
#     response = HttpResponse()
#     response['Content-Type'] = job.content_type
#     response['Content-Length'] = len(job.picture)
#     response.write(job.picture)
#     return response

# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class JobdFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        j = get_object_or_404(Job, id=pk)
        fav = Fav(user=request.user, job=j)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        j = get_object_or_404(Job, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, job=j).delete()
        except Fav.DoesNotExist as e:
            pass
        return HttpResponse()

