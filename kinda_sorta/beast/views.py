from django.shortcuts import render
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.template import loader, Context, RequestContext, Template

from beast.validater import validater
from beast.walters import walters

import random
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

	# Store the values of the object in a Session 
	request.session['title'] = flatData['Title']
	request.session['medium'] = flatData["Medium"]
	request.session['objectName'] = flatData['ObjectName']
	request.session['creators'] = flatData["Creators"]
	request.session['geography'] = flatData["Geographies"]

	json_obj = {"baseObj": 
				{ "title":flatData['Title'],
					"material":flatData["Medium"],
					"objectName":flatData["ObjectName"],
					"url":flatData["ResourceURL"],
					"img":flatData["Images"][0]["ImageURLs"]["Large"],
					"artist":flatData["Creators"],
					"geography":flatData["Geographies"],
				}
			}

	# renders stock result page
	# return render(request, 'results.html', json_obj)
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

		# Pass session variables 
		# def ks_query(self, id, mq, oq, mat_weight, objName_weight, mat_mm, objName_mm): 

		response = wam.getTestImages()
		t = loader.get_template('object_results.html')
		c = RequestContext( request, { 'response': response })
		return HttpResponse(t.render(c))

	except Exception as e:
		print ("Exception thrown")
		print (e)
		return HttpResponse("{vale:shit}","application/json")
"""
render error page
"""
def error(request):
	return render(request, 'error.html')





