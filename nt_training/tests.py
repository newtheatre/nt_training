# All the imports

## Global
import datetime

## Django
from django.test import TestCase
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse


############ NNT Training ##########
from .models import Icon, Person, Training_Spec, Training_Session
urls = 'nt_training.urls'

# Useful Functions

def createPerson(first_name,last_name,grad_year):
	full_name = first_name + ' ' + last_name
	slug = slugify(full_name)
	return Person.objects.create(
		first_name = first_name,
		last_name = last_name,
		slug = slug,
		grad_year = grad_year,
	)

def addToSpec(trainingId,category,trainingTitle,description,safety):
	return Training_Spec.objects.create(
		trainingId = trainingId,
		category = category,
		trainingTitle = trainingTitle,
		description = description,
		safety = safety,
	)

def addSession(trainingId,trainer,trainee,date):
	session = Training_Session.objects.create(trainer=trainer)
	session.trainee.add(trainee)
	session.trainingId.add(trainingId)
	return session

def addIcon(iconType,ref,name,weight,primary,description):
	return Icon.objects.create(
		itemType=iconType,
		iconRef=ref,
		iconName = name,
		weight = weight,
		primary = primary,
		description = description,
	)

# Tests

## /
class Test_NT_Home(TestCase):
# Unit tests for the home page

	### Should render as 200
	def test_nt_home200(self):
		url = reverse('nt_training:ntHome')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	### Should not list category icons
	def test_nt_iconCat(self):
		icon = addIcon('CAT','lighting','Lighting',1,True,'lighting fixtures and instruments')
		setattr(icon, 'viewName', 'ntPeople') 
		icon.save()
		url = reverse('nt_training:ntHome')
		response = self.client.get(url)
		self.assertNotContains(response,icon.description)

	### Should list pages with icons
	def test_nt_iconPage(self):
		icon = addIcon('PAGE','fa fa-users','People',1,True,'all the users')
		setattr(icon, 'viewName', 'ntPeople')
		icon.save()		
		
		url = reverse('nt_training:ntHome')
		response = self.client.get(url)
		self.assertContains(response,icon.description)

	### If there is both, should only list pages
	def test_nt_iconCatPage(self):
		iconPage = addIcon('PAGE','people','People',1,True,'details about the users')
		setattr(iconPage, 'viewName', 'ntPeople') 
		iconPage.save() 
		iconCAT = addIcon('CAT','lighting','Specific Category',1,True,'lighting fixtures and instruments')
		url = reverse('nt_training:ntHome')
		response = self.client.get(url)
		self.assertNotContains(response,iconCAT.description)
		self.assertNotContains(response,iconCAT.iconName) # Ensure it's not in the nav bar
		self.assertContains(response,iconPage.description)

	### Only display primary pages in panels
	def test_nt_iconPrimaryPage(self):
		iconPrimary = addIcon('PAGE','people','People',1,True,'details about the users')
		setattr(iconPrimary, 'viewName', 'ntPeople') 
		iconPrimary.save() 
		iconNot = addIcon('PAGE', 'about', 'About', 2, False, 'about this site')
		setattr(iconNot, 'viewName', 'ntAbout')
		iconNot.save()
		url = reverse('nt_training:ntHome')
		response = self.client.get(url)
		self.assertNotContains(response,iconNot.description)
		self.assertContains(response,iconPrimary.description)	
		#### But both should display in the nav bar
		self.assertContains(response,iconPrimary.iconName)	
		self.assertContains(response,iconNot.iconName)	

## /training
class Test_NT_Training_Category(TestCase):
# Unit tests for the plain category panels page
	'''
	Is it safe to assume that if these all pass, then the use of category panels in the 
	person page also passes, and then test for the specific differences there?
	'''
	### Should render as 200
	def test_nt_category200(self):
		url = reverse('nt_training:ntCategory')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	### Should show labels 
	def test_nt_categoryJumpLabels(self):
		iconLighting = addIcon('CAT','lightbulb-o','Lighting',1,True,'')
		url = reverse('nt_training:ntCategory')
		response = self.client.get(url)
		testString = '<p>Jump to: <a href="#Lighting" title="Lighting" class="filter label label-info">Lighting</a>'
		self.assertContains(response, testString)
	
	### Should show all categories, regardless of training within
	def test_nt_categoryIcons(self):
		iconLighting = addIcon('CAT','lightbulb-o','Lighting',1,True,'')
		url = reverse('nt_training:ntCategory')
		response = self.client.get(url)
		testString = '<i class="fa fa-fw fa-lightbulb-o"></i> Lighting'
		self.assertContains(response, testString)

	### Should show all training 
	def test_nt_category_show_training(self):
		iconLighting = addIcon('CAT','lightbulb-o','Lighting',1,True,'')
		training1 = addToSpec('1.01',iconLighting,'Basic lanterns','fixture operations',False)
		training2 = addToSpec('1.02',iconLighting,'Safe things','healthy safety basics',True)

		url = reverse('nt_training:ntCategory')
		response = self.client.get(url)
		self.assertContains(response, training1.trainingTitle)
		self.assertContains(response, training2.trainingTitle)
		#### Safety training has safety mark
		safetyString = '<i class="fa fa-exclamation-circle text-danger" aria-label="Exclamation point" title="Safety critical"></i>&nbsp;'
		self.assertContains(response, safetyString+training2.trainingTitle)
		#### Non-safety training does not have mark
		self.assertNotContains(response, safetyString+training1.trainingTitle)

	### Should display info message when there is no training
	def test_nt_category_no_training(self):
		iconLighting = addIcon('CAT','lightbulb-o','Lighting',1,True,'')
		url = reverse('nt_training:ntCategory')
		response = self.client.get(url)
		testString = '<i class="fa fa-info-circle fa-fw"></i> No training in this department.</td>'
		self.assertContains(response, testString)

	### Should place all training within its relevant category
	def test_nt_categoryTraining(self):
		return

	### Should show a data table if there is training spec items
	def test_nt_category_datatable(self):
		#### Should show a message if there is none 
		url = reverse('nt_training:ntCategory')
		response = self.client.get(url)
		testString = '<p><i class="fa fa-info-circle fa-fw"></i> There is no training.</p>'
		self.assertContains(response, testString)

	### Should produce a modal which shows who has trained and been trained 
	def test_nt_category_modal_training(self):
		lx = addIcon('CAT','fa fa-lightbulb-o','Lighting',1,False,'Lamps and fixtures')
		spec = addToSpec(1.01,lx,'Rigging Basics','Short Description',False)

		nonetaught = 'This has not been taught by anyone.'
		nonetrained = 'This has not been taught to anyone.'

		url = reverse('nt_training:ntCategory')
		response = self.client.get(url)

		self.assertContains(response, nonetaught)
		self.assertContains(response, nonetrained)

		trainer = createPerson('the','teacher',1999)
		trainee = createPerson('a','student',2001)
		session = addSession(spec,trainer,trainee,timezone.now())
		taughtTo = 'Has been taught to: <a href="/people/a-student/">'+str.title(trainee.first_name)
		taughtBy = 'Has been taught by: <a href="/people/the-teacher/">'+str.title(trainer.first_name)

		url = reverse('nt_training:ntCategory')
		response = self.client.get(url)
		self.assertContains(response, taughtTo)
		self.assertContains(response, taughtBy)

#/people
class Test_NT_People(TestCase):
# Unit tests for the people list page
	### Should render as 200
	def test_nt_people200(self):
		url = reverse('nt_training:ntPeople')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	### Should list all people
	def test_nt_peopleList(self):
		joe = createPerson('joe', 'bloggs', 2006)
		bill = createPerson('BiLL', 'PoTTs', 2016)
		doc = createPerson('doctor', 'who', 1963)
		cass = createPerson('cassandra',"o'brien", 2001)
		url = reverse('nt_training:ntPeople')
		response = self.client.get(url)
		self.assertContains(response, str.title(joe.first_name))
		self.assertContains(response, str.title(bill.first_name))
		self.assertContains(response, str.title(doc.last_name))
		self.assertContains(response, '<a href="/people/cassandra-obrien/">')
		self.assertContains(response, 'Cassandra O&#39;Brien')
		# By passing, we also confirm that all names display in titlecase and we deal with apostrophes appropriately.

	### Should list people's achievements
	def test_nt_peopleAchievements(self):
		joe = createPerson('joe','bloggs',2006)
		bill = createPerson('bill', 'potts', 2009)
		teach = createPerson('the','teacher',1999)

		# Set up for test
		iconLighting = addIcon('CAT','lightbulb-o','Lighting',1,True,'')
		training1 = addToSpec(1.01,iconLighting,'Basic lanterns','fixture operations',False)
		training2 = addToSpec(1.02,iconLighting,'Safe things','healthy safety basics',True)
		
		session1 = addSession(training1,teach,joe,timezone.now())
		session1.trainee.add(bill)

		url = reverse('nt_training:ntPeople')

		# At this point, no one has completed any department.
		response = self.client.get(url)
		labelTest = '<label class="label label-info">Lighting Technician</label>'
		self.assertNotContains(response, labelTest)

		session2 = addSession(training2,teach,joe,timezone.now())
		response = self.client.get(url) #Refresh
		# Joe completes one department
		self.assertContains(response, labelTest)
		# Need a method of testing that Joe has a label, but Bill does not when 
		# only one has completed the category

	def test_nt_people_graduate(self):
		## The people page should show graduated status, and nothing for non-graduates.
		person = createPerson('joe','bloggs',2006)
		url = reverse('nt_training:ntPeople')
		gradString = 'fa-graduation-cap'
		response = self.client.get(url)
		self.assertNotContains(response, gradString)

		setattr(person, 'status', 'GRAD')
		person.save()
		response = self.client.get(url)
		self.assertContains(response, gradString)

#/people/first-last
class Test_NT_Person(TestCase):
# Unit tests for the person detail page

	def test_nt_person200GradPast(self):
		## A person with a graduation year in the past will 200
		p = createPerson('joe','bloggs',2009)
		url = reverse('nt_training:ntPerson', args=(p.slug,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	def test_nt_person200GradFuture(self):
		## A person with a graduation year in the future will 200
		p = createPerson('joe','bloggs',2999)
		url = reverse('nt_training:ntPerson', args=(p.slug,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200) 

	def test_nt_person404(self):
		## A url with no person will 404
		p = 'joe-bloggs'
		url = reverse('nt_training:ntPerson', args=(p,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404) 

	def test_nt_person_training(self):
		## A person's detail page will show their completed training points
		joe = createPerson('joe','bloggs',2009)
		teach = createPerson('the','teacher',1999)
		iconLighting = addIcon('CAT','lightbulb-o','Lighting',1,True,'')
		training1 = addToSpec(1.01,iconLighting,'Basic lanterns','fixture operations',False)
		training2 = addToSpec(1.02,iconLighting,'Safe things','healthy safety basics',True)
		
		session1 = addSession(training1,teach,joe,timezone.now())

		url = reverse('nt_training:ntPerson', args=(joe.slug,))
		response = self.client.get(url)

		trainingGotString = '<tr class="clickme '+str(training1.category)+' success" data-toggle="modal" data-target="#'+str(training1.pk)+'-Modal"><td>'+str(training1.trainingId)+'</td>'
		trainingNotString = '<tr class="clickme '+str(training2.category)+' danger hidden" data-toggle="modal" data-target="#'+str(training2.pk)+'-Modal"><td>'+str(training2.trainingId)+'</td>'
		self.assertContains(response, trainingGotString) #Got training is green
		self.assertContains(response, trainingNotString) #Not training is red and hidden, both are in source

	def test_nt_person_no_training(self):
		## A person with no training should display counts as 0, rather than no counts
		joe = createPerson('joe','bloggs',2009)
		iconLighting = addIcon('CAT','lightbulb-o','Lighting',1,True,'')
		training1 = addToSpec(1.01,iconLighting,'Basic lanterns','fixture operations',False)
		training2 = addToSpec(1.02,iconLighting,'Safe things','healthy safety basics',True)

		countString = '<label class="label label-danger">0 / '
		# Also serves as testing for the colour, 0 has .label-warning
		url = reverse('nt_training:ntPerson', args=(joe.slug,))
		response = self.client.get(url)
		self.assertContains(response, countString)

	def test_nt_person_training_count(self):
		## A person's training count will show one count for each unique completed training ID
		joe = createPerson('joe','bloggs',2009)
		teach = createPerson('the','teacher',1999)
		teach2 = createPerson('another','teacher',2000)
		iconLighting = addIcon('CAT','lightbulb-o','Lighting',1,True,'')
		training1 = addToSpec(1.01,iconLighting,'Basic lanterns','fixture operations',False)
		training2 = addToSpec(1.02,iconLighting,'Safe things','healthy safety basics',True)
		
		session1 = addSession(training1,teach,joe,timezone.now())
		# Also serves as testing for the colour: user < spec has .label-warning 
		countString = '<label class="label label-warning">1 / 2'

		url = reverse('nt_training:ntPerson', args=(joe.slug,))
		response = self.client.get(url)

		self.assertContains(response, countString)

		## Count will not increase when trained on the same thing twice
		session2 = addSession(training1,teach2,joe,timezone.now())
		response = self.client.get(url)
		self.assertContains(response, countString)

		## But count will then increase to complete when category is completed
		session3 = addSession(training2,teach,joe,timezone.now())
		# Also serves as testing for the colour: user = spec has .label-success
		countComplete = '<label class="label label-success">2 / 2'
		response = self.client.get(url)
		self.assertContains(response, countComplete)

	def test_nt_person_no_training_count(self):
		## Counter should not appear when there is no training in a department (fringe case)
		joe = createPerson('joe','bloggs',2009)
		iconLighting = addIcon('CAT','lightbulb-o','Lighting',1,True,'')
		countString = '0 / 0'
		url = reverse('nt_training:ntPerson', args=(joe.slug,))
		response = self.client.get(url)
		self.assertNotContains(response, countString)

	def test_nt_person_graduated(self):
		## The person page should show the graduate status and year
		graduate = createPerson('joe','bloggs',2009)
		setattr(graduate, 'status', 'GRAD') 
		graduate.save()
		gradString = '<i class="fa fa-fw fa-inverse fa-graduation-cap" aria-label="Graduated in ""></i>'
		url = reverse('nt_training:ntPerson', args=(graduate.slug,))
		response = self.client.get(url)
		self.assertContains(response, gradString)

	def test_nt_person_student(self):
		## Should show student status for a student
		student = createPerson('joe','bloggs',2009)
		setattr(student, 'status', 'STU') 
		student.save()
		url = reverse('nt_training:ntPerson', args=(student.slug,))
		response = self.client.get(url)
		self.assertContains(response, 'Student')

	def test_nt_person_unknown(self):
		## Should show unknown if unknown
		person = createPerson('joe','bloggs',2009)
		url = reverse('nt_training:ntPerson', args=(person.slug,))
		response = self.client.get(url)
		self.assertContains(response, 'Unknown')

	def test_nt_person_training_table(self):
		## Multiple tests for the training table at the bottom of a person's page 

		### Should show messages when there is no training given or received 
		trainee = createPerson('joe','bloggs',2009)
		trainer = createPerson('the', 'teacher', 1990)
		iconLighting = addIcon('CAT','lightbulb-o','Lighting',1,True,'')
		training1 = addToSpec(1.01,iconLighting,'Basic lanterns','fixture operations',False)

		url = reverse('nt_training:ntPerson', args=(trainee.slug,))
		response = self.client.get(url)
		self.assertContains(response, 'has given no training')
		self.assertContains(response, 'has received no training')

		session1 = addSession(training1,trainer,trainee,timezone.now())
		### Should show table when there is training received. Table will contain trainer's name
		url = reverse('nt_training:ntPerson', args=(trainee.slug,))
		response = self.client.get(url)
		testString = str.title(trainer.last_name)+'</a></td>'
		self.assertContains(response, testString)

		### Should show table when there is training given. Table will contain trainee's name.
		url = reverse('nt_training:ntPerson', args=(trainer.slug,))
		response = self.client.get(url)
		testString = str.title(trainee.last_name)+'</a></td>'
		self.assertContains(response, testString)

class Test_NT_Sessions(TestCase):
	## Tests for the Sessions List page

	### Should render as 200
	def test_nt_sessions200(self):
		url = reverse('nt_training:ntSessions')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	### Should display message when there are no sessions, regardless of state of spec
	def test_nt_sessions_none(self):
		noneString = 'No training sessions.'
		url = reverse('nt_training:ntSessions')
		response = self.client.get(url)
		self.assertContains(response, noneString)

		p = createPerson('joe','bloggs',1990)
		lx = addIcon('CAT','lightbulb-o','Lighting',1,False,'Things')
		t = addToSpec(1.01,lx,'Lighting','Things',False)
		response = self.client.get(url)
		self.assertContains(response, noneString)

	### Should display the trainer, trainee and training spec item when there is a session
	def test_nt_sessions_some(self):
		noneString = 'No training sessions.'
		url = reverse('nt_training:ntSessions')

		p = createPerson('joe','bloggs',1990)
		p2 = createPerson('the','teacher',1992)
		lx = addIcon('CAT','lightbulb-o','Lighting',1,False,'Things')
		t = addToSpec(1.01,lx,'Lighting','Things',False)
		s = addSession(t,p,p2,timezone.now())

		response = self.client.get(url)
		self.assertNotContains(response, noneString)
		self.assertContains(response, p.first_name)
		self.assertContains(response, p2.first_name)
		self.assertContains(response, t.trainingId)
		

#Category panels: Test logic for if forms == false

#### should show prev/next when there is, and not when there is not

## /detail 
### Should render as 200
### Should show table
### Should show jump labels 
### Usage: When labels clicked, should appear in search box



## /training/id
### /training/bad-id should render as 404

### /training/good-id should render as 200 