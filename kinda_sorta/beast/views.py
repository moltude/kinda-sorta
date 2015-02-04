from django.shortcuts import render
from django.http import HttpResponse
from django.core.context_processors import csrf

import random
from beast.validater import validater
from beast.walters import walters

import json
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
Called from the landing page. Builds the default search results page which consists of:
1. Summary of the object searched for (image, metadata)
2. Related objects using the stock values.
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
Query Solr for related objects

"""
def query(request): 
	try : 
		ks = json.loads(request.POST.get('ks'))
		wam = walters()
		response = wam.getTestImages()
		return render(request, 'object_results.html', {
			'response': response, 
		})
	except Exception as e:
		print (e)
		return HttpResponse('NULL')

"""
render error page
"""
def error(request):
	return render(request, 'error.html')





