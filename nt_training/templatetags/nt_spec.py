from django import template
from django.db import models 
from django.db.models import Count
from ..models import Department, Icon, Person, Training_Session, Training_Spec

register = template.Library() 

# Template tags related to the training spec, and comparing other models to the spec (for completion)

def get_user_points(person, dept=None, gotsessions=None):
	# Gets a person's training IDs, only unique values
	# (avoids counting multiple training sessions as >1 signing offs)
	if gotsessions == None:
		# Only if the person's training sessions are not yet a variable
		personTraining = Training_Session.objects.filter(trainee=person).prefetch_related('trainingId')
	else:
		personTraining = gotsessions

	# Get the achieved training points
	userPoints = [] #Set up for population
	for session in personTraining: #Iterate over sessions a person is the trainee in
		alltraining = session.trainingId.all().select_related('category')
		for training in alltraining:
			# Either get the achieved training for a given dept, or all of it.
			if dept is not None:
				if training.category == dept:
					userPoints.append(training.pk)
			else:
				userPoints.append(training.pk)
	userPoints = set(userPoints) #Remove duplicates
	user_count = len(userPoints) #Just the number of achieved points is sufficient
	return user_count


@register.simple_tag
def tech_status(person, dept, count=False):
	'''
	Determine how many training points of a department a person is signed off on.
	
	Count returns a list with the two numbers, leaving the logic as the template's responsibility
	Setting count=False returns a boolean: are all completed or not? This is for a future feature.

	Future: Be able to filter people who have all of a department signed off.
	'''
	allspec = Training_Spec.objects.select_related('category') # Get all training points

	if dept is not None: # Filter to one department?
		spec_count = allspec.filter(category=dept).count()
	if person is None: #Used to check if there is actually training for a given department, should be >0
		return spec_count
	else: 
		user_count = get_user_points(person, dept)

	if count == True:
		statusList = (user_count, spec_count)
		return statusList
	else: # Used for listing a progression label
		if (spec_count == user_count) and (spec_count > 0):
			same = True
		else:
			same = False 
		return same 

@register.simple_tag
def session_status(session, dept):
	# Returns a dictionary, statusList, of the number of training points of a given department in the session
	# that are completed; and the total in the department

	allspec = Training_Spec.objects.select_related('category')
	spec_count = allspec.filter(category=dept).count() 
	if type(session) == Training_Session:
		session_count = session.objects.filter(category = dept).count() 
	elif type(session) == models.query.QuerySet:
		session_count = session.filter(category=dept).count() 

	statusList = (session_count, spec_count)

	return statusList


@register.inclusion_tag('nt_training/template_tags/training-card.html')
def training_cards(person=None, form=None, session_boxes=None):
	'''
	Display a view of training split into cards for each department.
	Person argument introduces colour-coding and counting based on 
	the person's achieved training points

	For a single view, session_boxes=object.trainingId.all (the boxes to be checked).

	Site usage:
		- Person: counters (expands), colour_bands, modals 
		- Session: counters (expands), colour_bands, modals
		- Session Form: checkboxes, 
		- Else (training page): modals

	'''

	# Initial card settings
	card_settings = dict.fromkeys(['counters', 'colour_bands', 'modals', 'checkboxes'], False)
	# Respectively: counter labels; green/red colour-coding, also implies expanding tables;
	# training point information modals; used when editing/creating a training session

	#Get the data to iterate and compare with 
	cats = Icon.objects.filter(itemType='CAT').order_by('department','weight').select_related('department')
	training = Training_Spec.objects.all().order_by('trainingId').select_related('category')
	departments = Department.objects.all().order_by('weight')
	if not departments:
		departments = ['no_depts']

	if person is not None: 
		# If we are dealing with a person, look at all the training they have been given
		# Return a list of the training points that they have been trained on

		# Settings for people:
		card_settings.update(dict.fromkeys(['counters','colour_bands','modals'], True))

		person_as_trainee = Training_Session.objects.filter(trainee=person).prefetch_related('trainingId')
		person_achieved_points = [] 
		for session in person_as_trainee:
			# For each session, get all the training and add it to the list 
			all_training = session.trainingId.all() 
			for training_ids in all_training:
				person_achieved_points.append(training_ids.trainingId)

		# Remove duplicates, in case a person is trained on one item more than once
		person_achieved_points = set(person_achieved_points) #Remove duplicates
		person_achieved_points = list(person_achieved_points) #Return to a list

		if person_achieved_points == []: 
			# If they have achieved no training, indicate this (rather than an unset variable)
			person_achieved_points = [0.00]

		return {
			'card_settings': card_settings,
			'departments': departments,
			'cats': cats, # All categories
			'training': training, # All training 
			'person': person, # The person 
			'person_achieved_points': person_achieved_points # Their achieved training 
		}
	
	elif session_boxes is not None: 
		# If we're viewing a training session, this variable represents the training covered 
		# in the given training session 
		card_settings.update(dict.fromkeys(['counters','colour_bands','modals'], True))

		return {
			'card_settings': card_settings,
			'departments': departments,
			'cats': cats, # All categories
			'training': training, # All training
			'session_boxes': session_boxes # The training covered 
		}

	elif form is not None: 
		# If we're creating or editing a training session, remove modals, colour bands and counters
		# Return the settings and the form items
		card_settings.update(dict.fromkeys(['checkboxes'], True))

		return {
			'card_settings': card_settings, 
			'departments': departments,
			'cats': cats, # All categories
			'training': training, # All training 
			'form': form 
		}

	else: 
		# Assume a simple training view is requested, so no bells and whistles
		card_settings.update(dict.fromkeys(['modals'], True))

		return { 
			'card_settings': card_settings,
			'departments': departments,
			'cats': cats,
			'training': training,
		}

''' 
	Old version:

	if person is not None:
		personTraining = Training_Session.objects.filter(trainee=person).prefetch_related('trainingId')
		achievedPoints = []
		for session in personTraining:
			allsession = session.trainingId.all() 
			for ids in allsession: 
				achievedPoints.append(ids.trainingId)
		achievedPoints = set(achievedPoints) #Remove duplicates
		achievedPoints = list(achievedPoints) #Return to a list
		if achievedPoints == []:
			achievedPoints = [0.00]
			# Ensure that those with no training are displayed as such
	else:
		achievedPoints = None 
	if form is not False: 
		inputForm = form
	else:
		inputForm = None 
	return {
		'cats': cats, #Categories 
		'training': training, #Training Spec 
		'achievedPoints': achievedPoints, #List of completed spec items 
		'person': person, #The person 
		'sessions': Training_Session.objects.all().prefetch_related('trainingId'), 
		'inputForm': inputForm, 
		'checked': checked, #Checked checkboxes
	}
''' 
