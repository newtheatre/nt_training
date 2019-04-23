# Tags relating to training sessions primarily.

from django import template
from ..models import Icon, Department, Person, Training_Session, Training_Spec

register = template.Library() 

@register.simple_tag
def person_trainee(person):
	# Returns a list of training sessions in which the person is a trainee
	sessions = Training_Session.objects.filter(trainee=person).order_by('date').prefetch_related('trainingId').select_related('trainer')
	return sessions

@register.simple_tag
def person_trained(person):
	# Returns a list of training sessions in which the person is a trainer
	trained = Training_Session.objects.filter(trainer=person).order_by('date').prefetch_related('trainingId').prefetch_related('trainee')
	return trained

@register.simple_tag
def id_people(spec):
	# Returns a list of who has trained, and who has been trained (current students only), on a certain training ID
	sessions = Training_Session.objects.filter(trainingId=spec).prefetch_related('trainee')
	trainers = []
	trainees = [] #Set up for population
	for session in sessions:
		session_trainees = session.trainee.filter(status='STU') #Only student trainees
		for t in session_trainees:
			trainees.append(t) #Populate
		trainers.append(session.trainer)

	#Remove duplicates
	trainers = set(trainers) 
	trainers = list(trainers)

	trainees = set(trainees)
	trainees = list(trainees)

	return {'trainers': trainers, 'trainees': trainees}

def ordered_set(seq):
	# From https://stackoverflow.com/a/480227 - remove duplicates and maintain order
  seen = set()
  seen_add = seen.add
  return [x for x in seq if not (x in seen or seen_add(x))]


@register.simple_tag
def session_meta(session):
	# Returns the list of categories covered in a given training session
	ids = session.trainingId.order_by('trainingId').select_related('category') #Get points
	session_cat_list = [] #For population later
	session_depts = []
	for trainingid in ids:
		session_cat_list.append(trainingid.category.iconRef) # Get a list of the categories involved
		session_depts.append(trainingid.category.department)
	session_cat_list = ordered_set(session_cat_list) #Preserve numerical order
	session_depts = ordered_set(session_depts)

	allcats = Icon.objects.filter(itemType = 'CAT') #All the training categories 
	session_cat_dict = {} #Dictionary for use in templates
	for cat in session_cat_list:
		this_cat_icon = allcats.get(iconRef = cat) # Get the list of icons 
		session_cat_dict[cat] = [this_cat_icon]

	return {'session_cat_dict': session_cat_dict, 'session_depts': session_depts}

@register.inclusion_tag('nt_training/template_tags/session-card.html')
def session_cards(sessions=None):
	# Display training sessions as panels
	# (also uses session_meta, above, in the inclusion tag)
	if sessions == None:
		# If no sessions are given, default to use all of them
		sessions = Training_Session.objects.all().prefetch_related('trainingId')

	departments = Department.objects.all()
	return {'sessions': sessions, 'departments': departments}
