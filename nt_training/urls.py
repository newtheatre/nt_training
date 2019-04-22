from django.urls import path

from . import views

app_name = 'nt_training'
urlpatterns = [

	# Authentication
	#/login
	path('login/', views.NTLoginView.as_view(), name='ntLogin'),
	#/logout
	path('logout/', views.NTLogoutView.as_view(), name='ntLogout'),
	#/user
	path('user/done/', views.NTUserEditDone.as_view(), name='ntUserEditDone'),
	path('user/', views.NTUserEdit.as_view(), name='ntUserEdit'),

	#/
	path('', views.HomeView.as_view(), name='ntHome'),

	# People Views
	#/people
	path('people/', views.PeopleView.as_view(), name='ntPeople'),
	#/people/slug
	path('people/<slug:slug>', views.PersonView.as_view(), name='ntPerson'),
	
	# Training Spec Views
	#/training
	path('training/', views.TrainingView.as_view(), name='ntCategory'),
	#/training/id
	path('training/<int:pk>/', views.TrainingDetailView.as_view(), name='ntTrainingDetail'),

	# Training Session Views
	#/training/session (List view)
	path('training/session/', views.SessionView.as_view(), name='ntSessions'),
	#/training/session/id (Single view)
	path('training/session/<int:pk>/', views.SessionSingleView.as_view(), name='ntSessionSingle'),
	## Login required (handled in views.py)
	#/training/session/new (Create view)
	path('training/session/new/', views.SessionNewView.as_view(), name='ntSessionNew'),
	#/training/session/id/edit (Update view)
	path('training/session/<int:pk>/edit/', views.SessionEditView.as_view(), name='ntSessionEdit'),

	# About Page 
	#/about
	path('about/', views.AboutView.as_view(), name='ntAbout'),

]
handler404 = views.PageNotFoundView.as_view()