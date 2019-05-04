from django.contrib import admin, messages
from django.db import models 
from django.forms import CheckboxSelectMultiple

# Register your models here.

from .models import Department, Icon, Person, Training_Session, Training_Spec

class PersonAdmin(admin.ModelAdmin):
	fields = ['first_name', 'last_name','slug','email','status','grad_year', 'committee', 'is_trainer']
	prepopulated_fields = {"slug": ("first_name", "last_name",)}
	list_display = ('slug', 'first_name', 'last_name', 'email','status', 'grad_year', 'committee', 'is_trainer')
	search_fields = ['first_name', 'last_name', 'grad_year', 'email']
	list_filter = ['status', 'grad_year', 'committee', 'is_trainer']

	def make_graduated(modeladmin, request, queryset):
		queryset.update(status='GRAD')
	def make_student(modeladmin, request, queryset):
		queryset.update(status='STU')
	def make_unknown(modeladmin, request, queryset):
		queryset.update(status='UNKNOWN')
	def toggle_committee(modeladmin, request, queryset):
		for person in queryset:
			if person.committee == False:
				setattr(person, 'committee', True)
			elif person.committee == True:
				setattr(person, 'committee', False)
			person.save() 
	def toggle_trainer(modeladmin, request, queryset):
		for person in queryset:
			if person.is_trainer == False:
				setattr(person, 'is_trainer', True)
			elif person.is_trainer == True:
				setattr(person, 'is_trainer', False)
			person.save() 

	actions = [make_graduated,make_student,make_unknown, toggle_committee, toggle_trainer]

class TrainingSpecAdmin(admin.ModelAdmin):
	list_filter = ['category']
	list_display = ['trainingId', 'category', 'trainingTitle', 'description', 'safety']

	def toggle_safety(modeladmin, request, queryset):
		for item in queryset:
			if item.safety == False:
				# item.update(safety=True)
				setattr(item, 'safety', True)
				item.save()  
			elif item.safety == True:
				# item.update(safety=False)
				setattr(item, 'safety', False)
				item.save()

	actions = [toggle_safety]

class TrainingSessionAdmin(admin.ModelAdmin):
	list_display = ['pk','trainer', '__str__', 'date',]
	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
	}
	list_filter = ['date','trainee','trainer']

# Dynamic actions for adding bulk adding categories to departments
# Creates actions by iterating over the departments 
def add_to_dept_action(department):
	def add_to_dept(modeladmin, request, queryset):
		for category in queryset: 
			setattr(category, 'department', department)
			category.save() 
			messages.info(request, "{0} added to {1}.".format(category, department))

	add_to_dept.short_description = "Add to {0}".format(department)
	add_to_dept.__name__ = "add_to_dept_{0}".format(department.pk) #Each action must be uniquely named

	return add_to_dept

class IconAdmin(admin.ModelAdmin):
	prepopulated_fields = {"description": ("iconName",)}
	list_display = ['itemType', 'department', 'weight', 'iconName', 'iconRef']
	list_filter = ['itemType']

	def get_actions(self, request):
		actions = super(IconAdmin, self).get_actions(request)

		for dept in Department.objects.all():
			action = add_to_dept_action(dept)
			actions[action.__name__] = (action, action.__name__, action.short_description)

		return actions

class DepartmentAdmin(admin.ModelAdmin):
	list_display = ['name', 'department_icon', 'person', 'email', 'weight']

admin.site.register(Person, PersonAdmin)
admin.site.register(Training_Session, TrainingSessionAdmin)
admin.site.register(Training_Spec, TrainingSpecAdmin)
admin.site.register(Icon, IconAdmin)
admin.site.register(Department, DepartmentAdmin)