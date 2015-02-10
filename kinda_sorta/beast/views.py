from django.shortcuts import render
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.template import loader, Context, RequestContext, Template

from beast.validater import validater
from beast.walters import walters
from beast.corona import corona

import random
import json
import string

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
This method was basically copeid and pased from results; 
TODO :: Pull elements into a single function
"""
def getRandomObject(request):
	solr = corona()
	objectId = solr.getRandom()
	# if we can get a valid objectId from the URL then we need to get
	# the object info from WaltersAPI
	wam = walters()
	try: 
		data = wam.getObject(objectId)
		flatData = wam.flatten(data)
	except Exception as e:
		print (e)
		return error(request)

	# This whole section seems a bit ridiculous but whatever..atm
	# Store the values of the object in a Session 
	replace_punctuation = str.maketrans(string.punctuation, ' '*len(string.punctuation))
		
	request.session['title'] = flatData['Title'].translate(replace_punctuation)
	request.session['medium'] = flatData["Medium"].translate(replace_punctuation)
	request.session['objectName'] = flatData['ObjectName'].translate(replace_punctuation)
	request.session['creators'] = flatData["Creators"].translate(replace_punctuation)
	request.session['geography'] = flatData["Geographies"].translate(replace_punctuation)
	request.session['keywords'] = flatData["Keywords"]
	request.session['description'] = flatData["Description"]

	json_obj = {"baseObj": 
				{ 	"title":flatData['Title'],
					"material":flatData["Medium"],
					"objectName":flatData["ObjectName"],
					"url":flatData["ResourceURL"],
					"img":flatData["Images"][0]["ImageURLs"]["Large"],
					"artist":flatData["Creators"],
					"geography":flatData["Geographies"],
					"keywords":flatData["Keywords"],
					"description":flatData["Description"],
				}
			}
	# renders stock result page
	t = loader.get_template('results.html')
	c = RequestContext(request, json_obj)
	return HttpResponse(t.render(c))

"""
Called from the landing page. Builds the default search results page which consists of:
1. Summary of the object searched for (image, metadata)
2. Related objects using the stock values.
"""
def results(request):
	print (request)
	# is there a query parameter? 
	if 'q' in request.GET:
		url = request.GET['q']
	else:
		# Return an error page
		return error(request)
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
		flatData = wam.flatten(data)

	except Exception as e:
		print (e)
		return error(request)

	# This whole section seems a bit ridiculous but whatever..atm
	# Store the values of the object in a Session 
	replace_punctuation = str.maketrans(string.punctuation, ' '*len(string.punctuation))
		
	request.session['title'] = flatData['Title'].translate(replace_punctuation)
	request.session['medium'] = flatData["Medium"].translate(replace_punctuation)
	request.session['objectName'] = flatData['ObjectName'].translate(replace_punctuation)
	request.session['creators'] = flatData["Creators"].translate(replace_punctuation)
	request.session['geography'] = flatData["Geographies"].translate(replace_punctuation)
	request.session['keywords'] = flatData["Keywords"]
	request.session['description'] = flatData["Description"]

	json_obj = {"baseObj": 
				{ 	"title":flatData['Title'],
					"material":flatData["Medium"],
					"objectName":flatData["ObjectName"],
					"url":flatData["ResourceURL"],
					"img":flatData["Images"][0]["ImageURLs"]["Large"],
					"artist":flatData["Creators"],
					"geography":flatData["Geographies"],
					"keywords":flatData["Keywords"],
					"description":flatData["Description"],
				}
			}

	# renders stock result page
	t = loader.get_template('results.html')
	c = RequestContext(request, json_obj)
	return HttpResponse(t.render(c))

"""
Query Solr for related objects

"""
def query(request): 
	try : 
		ks = json.loads(request.POST.get('ks'))
		wam = walters()

		# response = wam.getTestImages()
		# BASE_OBJ values are SESSION
		# KS_VALS are in ks

		response = wam.getKindaSortaObjects(ks=ks,baseObj=request.session)

		t = loader.get_template('object_results.html')
		c = RequestContext( request, { 'response': response })

		return HttpResponse(t.render(c))

	except Exception as e:
		print ("Exception thrown in VIEW.QUERY")
		print (e)
		return None
"""
render error page
"""
def error(request):
	return render(request, 'error.html')


def solr(request):
	solr = corona()
	return HttpResponse('Returned: %s' % solr.ping() )




