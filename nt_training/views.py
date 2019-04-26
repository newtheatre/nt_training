# Django includes
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.functions import Lower
from django.forms.models import modelformset_factory
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

# DB Includes
from .models import Department, Icon, Person, Training_Session, Training_Spec

# Forms
from .forms import SessionForm

# NNT Training Views

class PageNotFoundView(generic.ListView):
	template_name = "nt_training/404.html"

class HomeView(generic.ListView):
	model = Icon
	template_name = "nt_training/index.html"
	context_object_name = "page_list"
	def get_queryset(self):
		# Exclude training categories
		return Icon.objects.filter(itemType='PAGE')

class AboutView(generic.TemplateView):
	model = Icon
	template_name = "nt_training/about.html"

	def get_context_data(self):
		context = {} 
		context['Icon'] = Icon.objects.all() 
		context['departments'] = Department.objects.all()

		return context

class PeopleView(generic.ListView):
	template_name = "nt_training/people.html"
	model = Person
	context_object_name = "context"

	def get_context_data(self):
		context = {}
		# Get all the people. Lower required to allow for mixed-case in DB
		context['people'] = Person.objects.all()
		# Get the training categories
		context['cats'] = Icon.objects.filter(itemType='CAT').order_by('weight').only('iconName')
		context['departments'] = Department.objects.all()
		return context

class PersonView(generic.DetailView):
	template_name = "nt_training/people-single.html"
	model = Person

class TrainingView(generic.ListView):
	model = Training_Spec
	template_name = "nt_training/training.html"
	context_object_name = "training"

class TrainingDetailView(generic.DetailView):
	template_name = "nt_training/training-detail.html"
	model = Training_Spec
	context_object_name = "item"

class SessionView(generic.ListView):
	template_name = "nt_training/session.html"
	model = Training_Session
	def get_queryset(self):
		sessions = Training_Session.objects.order_by('-date')
		return sessions 
	context_object_name = "sessions"

class SessionSingleView(generic.DetailView):
	model = Training_Session
	template_name = "nt_training/session-single.html"

def is_nt_staff(user):
	return user.groups.filter(name='NT Staff').exists()


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_nt_staff), name='dispatch')
class SessionNewView(SuccessMessageMixin, CreateView):
	model = Training_Session
	form_class = SessionForm
	template_name = "nt_training/session-form.html"
	success_message = "Session created successfully."

	def get_success_url(self):
		return reverse_lazy('nt_training:ntSessionSingle', kwargs={'pk': self.object.pk })

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_nt_staff), name='dispatch')
class SessionEditView(SuccessMessageMixin, UpdateView):
	model = Training_Session
	form_class = SessionForm
	template_name = "nt_training/session-form.html"
	success_message = "Session edited successfully."

	def get_success_url(self):
		return reverse_lazy('nt_training:ntSessionSingle', kwargs={'pk': self.object.pk})

# Auth Views

class NTLoginView(auth_views.LoginView):
	template_name = "nt_training/login.html"


class NTLogoutView(auth_views.LogoutView):
	extra_context = {'logged_out': True }
	template_name = "nt_training/index.html"

# Already have login_required inherently
class NTUserEdit(auth_views.PasswordChangeView):
	template_name = "nt_training/user-edit.html"
	def get_success_url(self):
		return reverse_lazy('nt_training:ntUserEditDone')

class NTUserEditDone(auth_views.PasswordChangeDoneView):
	template_name = "nt_training/user-edit-done.html"

# Flash Messages

def logged_in_message(sender, user, request, **kwargs):
    # Add a welcome message when the user logs in
    messages.success(request, "Login successful!")
def logged_out_message(sender, user, request, **kwargs):
    # Add a welcome message when the user logs in
    messages.info(request, "You have logged out.")

user_logged_in.connect(logged_in_message)
user_logged_out.connect(logged_out_message)