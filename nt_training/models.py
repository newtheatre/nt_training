import datetime

from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone

# Create your models here.

# NNT Training Models

class Icon(models.Model):
	itemType = models.CharField(
		max_length=15,
		choices = (
			('PAGE', 'Page'),
			('CAT', 'Training Category'),
		),
	)
	iconRef = models.CharField(
		max_length=25,
		verbose_name = "Icon Code"
	)
	iconRef.short_description = "Icon Code"
	iconName = models.CharField(max_length=25)
	weight = models.IntegerField()
	primary = models.BooleanField(default=False)
	description = models.TextField(
		null=True,
		blank=True,
	)
	viewName = models.CharField(
		max_length=25,
		null=True,
		blank=True,
		default=None
	)
	def __str__(self):
		if self.itemType == 'PAGE':
			return self.iconName #+ ' (' + str(self.weight) + ')'
		elif self.itemType == 'CAT':
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
	slug = models.SlugField(
		max_length=100,
		null = True,
		unique = True,
	)
	slug.short_description = "Name"
	def __str__(self):
		full_name = self.first_name + ' ' + self.last_name
		full_name = str.title(full_name)
		return full_name

	class Meta:
		ordering = ['last_name', 'first_name']
		

class Training_Spec(models.Model):
	trainingId = models.DecimalField(
		max_digits = 4,
		decimal_places = 2,
		unique = True,
	)
	category = models.ForeignKey(
		Icon,
		limit_choices_to={'itemType': 'CAT'})
	trainingTitle = models.CharField(max_length=50)
	description = models.TextField(default="Provide a useful description")
	safety = models.BooleanField(default=False)
	def __str__(self):
		humanTitle = str(self.trainingId) + ' - ' +  self.trainingTitle
		return humanTitle

Training_Spec.short_description = "Training Specification"

class Training_Session(models.Model):
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
