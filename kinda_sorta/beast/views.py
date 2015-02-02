from django.shortcuts import render
from django.http import HttpResponse

import random
from beast.validater import validater
from beast.walters import walters
# Create your views here.

"""
The landing page for Kinda-Sorta
Displays a random image each time
"""
def index(request):
	# pick a random image from the list
	bg_imgs=['bg-01.jpg','bg-02.jpg','bg-03.jpg','bg-04.jpg','bg-05.jpg','bg-06.jpg','bg-07.jpg']
	index = random.randint(0, len(bg_imgs)-1)
	return render(request, 'index.html', {'bg':bg_imgs[index]} )

"""
Display the similar objects for a Walters Art Museum object
"""
def results(request):
	# is there a query parameter? 
	if 'q' in request.GET:
		url = request.GET['q']
	else:
		# Return an error page
		return render(request, 'results.html')
	# next validate the q
	try:
		url_valid = validater()
		objectId = url_valid.validate(url)
	except Exception as e:
		print (e) # TODO :: Log this better 
		return error(request)

	# if we can get a valid objectId from the URL then we need to get
	# the object info from WaltersAPI
	wam = walters()
	try: 
		data = wam.getObject(objectId)
	except Exception as e:
		print (e)
		return error(request)

	# renders stock result page
	return render(request, 'results.html', 
		{'baseObj': 
			{ 	'title':data['Title'],
				'material':data['Medium'],
				'objectName':data['ObjectName'],
				'url':data['ResourceURL'],
				'img':data['Images'][0]['ImageURLs']['Large']
			}
		})

"""
render error page
"""
def error(request):
	return render(request, 'error.html')





