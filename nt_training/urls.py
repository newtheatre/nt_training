from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'nt_training'
urlpatterns = [

	# Authentication
	#/login
	url(r'^login/$', views.NTLoginView.as_view(), name='ntLogin'),
	#/logout
	url(r'^logout/$', views.NTLogoutView.as_view(), name='ntLogout'),
	#/user
	url(r'^user/done/$', views.NTUserEditDone.as_view(), name='ntUserEditDone'),
	url(r'^user/$', views.NTUserEdit.as_view(), name='ntUserEdit'),

	#/
	url(r'^$', views.HomeView.as_view(), name='ntHome'),

	# People Views
	#/people
	url(r'^people/$', views.PeopleView.as_view(), name='ntPeople'),
	#/people/slug
	url(r'^people/(?P<slug>[\w\-]+)/$', views.PersonView.as_view(), name='ntPerson'),
	
	# Training Spec Views
	#/training
	url(r'^training/$', views.TrainingView.as_view(), name='ntCategory'),
	#/training/id
	url(r'^training/(?P<trainingId>[0-9]+)/$', views.TrainingIdView.as_view(), name='ntTrainingId'),

	# Training Session Views
	#/training/session (List view)
	url(r'^training/session/$', views.SessionView.as_view(), name='ntSessions'),
	#/training/session/id (Single view)
	url(r'^training/session/(?P<pk>[0-9]+)/$', views.SessionSingleView.as_view(), name='ntSessionSingle'),
	## Login required (handled in views.py)
	#/training/session/new (Create view)
	url(r'^training/session/new/$', views.SessionNewView.as_view(), name='ntSessionNew'),
	#/training/session/id/edit (Update view)
	url(r'^training/session/(?P<pk>[0-9]+)/edit/$', views.SessionEditView.as_view(), name='ntSessionEdit'),

	# About Page 
	#/about
	url(r'^about/$', views.AboutView.as_view(), name='ntAbout'),

]
handler404 = views.PageNotFoundView.as_view()