import datetime

from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone

# Create your models here.

# NNT Training Models

class Department(models.Model):
	class Meta:
		ordering = ['weight']

	name = models.CharField(
		verbose_name = "Department Name",
		max_length = 50
	)
	person = models.CharField(
		help_text = "Person in charge of the department",
		max_length = 50
	)
	email = models.EmailField(
		help_text = "Email address of the person in charge"
	)
	weight = models.IntegerField(
		unique = True 
	)
	department_icon = models.CharField(
		max_length=25,
		verbose_name = "Icon Code",
		default="fa fa-",
		help_text = 'From <a href="https://fontawesome.com/icons?d=gallery&m=free">Font Awesome 5</a>. Example: <code>fas fa-user</code>.'
	)
	def __str__(self):
		return str(self.name)

class Site_Page(models.Model):
	class Meta:
		verbose_name = "Site Page"
		ordering = ['weight']
	page_title = models.CharField(
		max_length = 25,
	)
	weight = models.IntegerField()
	primary = models.BooleanField(default=False)
	viewName = models.CharField(max_length=25)
	description = models.TextField(
		null=True,
		blank=True,
	)
	iconRef = models.CharField(
		max_length=25,
		verbose_name = "Icon Code",
		help_text = 'From <a href="https://fontawesome.com/icons?d=gallery&m=free">Font Awesome 5</a>. Example: <code>fas fa-user</code>.'
	)
	iconRef.short_description = "Icon Code"
	def __str__(self):
		return self.page_title

class Category(models.Model):
	class Meta:
		ordering = ['weight']
		verbose_name = "Training Category"
		verbose_name_plural = "Training Categories"

	iconRef = models.CharField(
		max_length=25,
		verbose_name = "Icon Code",
		help_text = 'From <a href="https://fontawesome.com/icons?d=gallery&m=free">Font Awesome 5</a>. Example: <code>fas fa-user</code>.'
	)
	iconRef.short_description = "Icon Code"
	iconName = models.CharField(
		max_length=25,
		verbose_name = 'Category Name'
	)
	weight = models.IntegerField()
	department = models.ForeignKey(
		Department,
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
		help_text = "Department this category belongs to. If you're using departments, you <strong>must</strong> set this for the category to appear."
	)
	description = models.TextField(
		null=True,
		blank=True,
	)
	def __str__(self):
		return str(self.weight) + '. ' + self.iconName

class Person(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	grad_year = models.IntegerField(null=True,blank=True,)
	committee = models.BooleanField(default=False)
	email = models.EmailField(
		null=True,
		# default=None,
	 	blank=True,
	)
	status = models.CharField(
		max_length = 15,
		choices = (
			('GRAD', 'Graduated'),
			('STU', 'Student'),
			('UNKNOWN', 'Unknown')
		),
		null = False,
		default='UNKNOWN'
	)
	is_trainer = models.BooleanField(
		default=False,
		help_text="Tick if this person trains others."
	)
	slug = models.SlugField(
		max_length=100,
		null = True,
		unique = True,
	)
	slug.short_description = "Name"
	def __str__(self):
		full_name = self.first_name + ' ' + self.last_name
		#full_name = str.title(full_name)
		return full_name

	class Meta:
		ordering = ['last_name', 'first_name']
		

class Training_Spec(models.Model):
	class Meta:
		verbose_name = "Training Specification"
		ordering = ['category', 'trainingId']

	trainingId = models.DecimalField(
		max_digits = 4,
		decimal_places = 2,
		unique = True,
	)
	category = models.ForeignKey(
		Category,
		on_delete=models.DO_NOTHING,
	)
	trainingTitle = models.CharField(
		max_length=50,
		verbose_name = "Training Title"
	) 
	description = models.TextField(default="Provide a useful description")
	safety = models.BooleanField(
		default=False,
		help_text = "Tick if training point has a health and safety element, or requires a period of supervision before signing off."
	)

	def __str__(self):
		humanTitle = str(self.trainingId) + ' - ' +  self.trainingTitle
		return humanTitle

class Training_Session(models.Model):
	class Meta:
		verbose_name = "Training Session"

	trainingId = models.ManyToManyField(Training_Spec)
	trainer = models.ForeignKey(Person, on_delete=models.DO_NOTHING, related_name="trainer")
	trainee = models.ManyToManyField(Person, related_name="trainee")
	date = models.DateField(
		default = datetime.date.today
	)
	def __str__(self):
		trainees = [] 
		for person in self.trainee.all():
			name = str.title(person.first_name) + ' ' + (str.title(person.last_name))
			trainees.append(name)
		string = str.title(self.trainer.first_name + ' ' + self.trainer.last_name) + ' taught ' + ', '.join(map(str,trainees))
		return string

	def get_absolute_url(self):
		return reverse('nt_training:ntSessions', kwargs={'pk': self.pk})

	def get_students(self):
		return self.trainee.all().filter(status='STU')
