#Import
##Global
import datetime
##Django
from django import forms 
from django.urls import reverse
##DB
from .models import Icon, Training_Spec, Person, Training_Session

class DateInput(forms.DateInput):
		input_type = 'date'

class SessionForm(forms.ModelForm):
	# Model: Training_Session. All of these fields are within this model. 
	class Meta:
		model = Training_Session
		fields = ['trainer', 'trainee', 'trainingId', 'date']
		labels = {
			'trainingId': 'Training Points',
			'trainee': 'People Trained',
			'trainer': 'Trainer'
		}
		widgets = {
			'date': DateInput(),
			'trainingId': forms.CheckboxSelectMultiple(),
			'trainee': forms.CheckboxSelectMultiple(),
		}

	def __init__(self, *args, **kwargs):
		super(SessionForm, self).__init__(*args, **kwargs)
		self.fields['trainer'].queryset = Person.objects.filter(is_trainer=True)

	def clean(self):
		trainee = self.cleaned_data.get('trainee')
		trainingId = self.cleaned_data.get('trainingId')
		trainer = self.cleaned_data.get('trainer')
		errors = {}
		# Can't submit without a valid trainer or date, so don't need to validate those.
		if trainee is None:
			errors['trainee'] = forms.ValidationError('Please select some trainees.')
		if trainingId is None:
			errors['trainingId'] = forms.ValidationError("You can't have a session without something to learn. Please select some training points.")
		if trainee is not None:
			if trainer in trainee.all(): # But the trainer should not be in the list of trainees.
				errors['trainer'] = forms.ValidationError("The trainer can't train themselves!")

		if errors:
			raise forms.ValidationError(errors)
			return self.cleaned_data
		
		# return self.cleaned_data

