import json
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def wesh(request):
	return json.dumps({'message' : 'wesh'})