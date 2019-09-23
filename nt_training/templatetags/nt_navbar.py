from django import template
from ..models import Site_Page

register = template.Library() 

# Template tags related to navigation

@register.inclusion_tag('nt_training/template_tags/nav.html')
def nav_items():
	# Returns all the pages by their order
	items = Site_Page.objects.all().order_by('weight')
	return {'items': items}

@register.simple_tag
def cat_items():
	# Returns all the categories by their order
	items = Category.objects.all().order_by('weight')
	return items