from django import template
from ..models import Icon

register = template.Library() 

# Template tags related to navigation

@register.inclusion_tag('nt_training/template_tags/nav.html')
def nav_items():
	# Returns all the pages by their order
	items = Icon.objects.filter(itemType='PAGE').order_by('weight')
	return {'items': items}

@register.simple_tag
def cat_items():
	# Returns all the categories by their order
	items = Icon.objects.filter(itemType='CAT').order_by('weight')
	return items