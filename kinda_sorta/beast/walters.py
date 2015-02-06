

"""
Class for interacting with Walters API
"""
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import quote_plus
import json
import os
from django.conf import settings
import random
import pprint

class walters():

	pp = pprint.PrettyPrinter(indent=4)

	"""	
	API paramters 
	"""
	walters_base_url = 'http://api.thewalters.org/v1/objects'

	HEROKU = bool(os.environ.get('HEROKU', ''))
	if HEROKU:
		api_key = os.environ['walters']
	if not HEROKU:
		api_key = settings.API_KEYS['walters']

	classifications = [ 
		'Miniatures',
		# commented out for test runs
		'Stained & Painted Glass','Lacquer & Inlay','Ceramics',
		'Precious Stones & Gems','Pearl, Horn, Coral & Shell'
		'Sculpture','Textiles','Painting & Drawing','Prints',
		'Coins & Medals','Arms & Armor','Mosaics & Cosmati','Niello',
		# 'Paper & Paper-Mache',
		'Wood','Enamels','Manuscripts & Rare Books',
		'Ivory & Bone','Mummies & Cartonnage','Timepieces, Clocks & Watches',
		'Glasswares','Metal','Gold, Silver & Jewelry','Stone','Resin, Wax & Composite',
		'Leather'
		]

	"""
	Returns JSON object from Walters API
	"""
	def getObject(self, objectId):
		url = self.walters_base_url + '/' + str(objectId) + '?' + 'apikey=' + self.api_key
		try:
			response = urlopen(url).read().decode("utf-8")
		except HTTPError as e:
			raise Exception('Unable to fetch object from ' + url)
		data = json.loads(response)
		return data['Data']

	"""
	There are several nested fields within the Walters API response which should be
	flatten out for HTML display

	This will be done on a specific field-by-field basis

	TODO :: Rewrite and cleanup
	"""
	def flatten(self, data):
		creators = [] 
		geoTerms = []
		# Flatten Creator
		if 'Creators' in data and data['Creators'] is not None: 
			for creator in data['Creators']:
				creators.append(creator['ConcatDisplayName'])			
			data['Creators'] = self.prettyString(creators)

		# Flatten Geographies
		if 'Geographies' in data and data['Geographies'] is not None: 
			for geo in data['Geographies']:
				geoTerms.append(geo['GeographyTerm'])
			data['Geographies'] = self.prettyString(geoTerms)

		return data

	"""
	Make it all pretty with commas and and's
	"""
	def prettyString(self, strArray):
		commaStr = "|".join(strArray)
		if '|' in commaStr:
			# replace last comma with an ' and '
			k = commaStr.rfind("|")
			commaStr = commaStr[:k] + " and " + commaStr[k+1:]
		return commaStr.replace('|', ', ')

	"""
	Pulls in random images for testing purposes 
	"""
	def getTestImages(self):
		objects = []
		url = self.walters_base_url + '/' + '?' + '&Classification=' + \
		quote_plus(random.choice(self.classifications)) + \
		'&apikey=' + self.api_key
		try:
			response = urlopen(url).read().decode("utf-8")
		except HTTPError as e:
			raise Exception('Unable to fetch object from ' + url)
		data = json.loads(response)
		items = data['Items']
		for item in items:
			obj = {}
			obj['imgUrl'] = item['PrimaryImage']['Large']
			obj['objUrl'] = item['ResourceURL']
			obj['objNumber'] = item['ObjectNumber']

			objects.append(obj)

		return {'objects': objects}

	def ks_query(self, id, mq, oq, mat_weight, objName_weight, mat_mm, objName_mm): 
		url = self.solrServer + '/query?q='\
		+ urllib.quote_plus('ks_how:'+ mq \
		+ ' AND ks_what:' + oq) \
		+ '&qf=ks_how^' + str(mat_weight) \
		+ '&qf=ks_what^' + str(objName_weight) \
		+ '&wt=json&indent=true'
		
		print (url)
		
		response = json.load(urllib.request.urlopen(url))
		
		for docs in response['response']['docs']:
			print ('MATERIAL: ' + docs['material'].encode('utf-8'))
			print ('OBJECT NAME: '+ docs['objectName'].encode('utf-8'))
			print ('--')




