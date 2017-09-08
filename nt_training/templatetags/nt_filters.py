from django import template

register = template.Library() 

# Utility template tags

@register.filter
def return_item(l, i):
	# Return the given index of a variable (useful to use as a pipe when directly indexing isn't possible)
	# Use case: Indexing a variable where the index is forloop.counter0
    try:
        return l[i]
    except:
        return None