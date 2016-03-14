from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

"""
@register.filter(is_safe=True)
def name(parm, arg2=default):
	#dost
	#for escape html --> escape()
"""

@register.filter
def last_word(sentance):

	sentance = sentance.split(' ')
	last = sentance[-1]

	return last