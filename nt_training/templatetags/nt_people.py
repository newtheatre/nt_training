from django import template
from django.db import models 
from ..models import Person

register = template.Library() 

# Template tags relating to people

@register.simple_tag
def all_people():
	# Get all the people 
	people = Person.objects.all() 
	return people 
