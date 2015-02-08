

"""
Class for interacting with Walters API
"""
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import quote_plus
from django.conf import settings
from beast.corona import corona

from concurrent import futures

import json
import os
import random
import pprint


class walters():

	pp = pprint.PrettyPrinter(indent=4)

	"""	
	API paramters 
	"""
	walters_base_url = 'http://api.thewalters.org/v1/objects'

	HEROKU = bool(os.environ.get('ON_HEROKU', ''))
	if HEROKU:
		api_key = os.environ['WALTERS_API_KEY']
	if not HEROKU:
		api_key = settings.API_KEYS['WALTERS_API_KEY']

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
		try:
			url = self.walters_base_url + '/' + str(objectId) + '?' + 'apikey=' + self.api_key
			try:
				response = urlopen(url).read().decode("utf-8")
			except HTTPError as e:
				raise Exception('Unable to fetch object from ' + url)
			data = json.loads(response)
			return data['Data']
		except Exception as e: 
			print ('ERROR -- getObject ' + str(objectId))
			print (e)
			return None

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

	"""
	Is passed the current KS values and base object metadata 
	Calls ks_query in the Corona class 
	Recieves results for ks_query (which is only objectId of results)
	Queries WaltersAPI to get images for those results
	Passes nicely formed JSON back to VIEWS.QUERY() <--- see getTestImages
	"""
	def getKindaSortaObjects(self, ks, baseObj):
		try:
			queryTerms = {
				'ks_what': baseObj['title'] + ' ' + baseObj['objectName'],
				'ks_how': baseObj['medium'],
				'ks_who': baseObj['creators'],
				'ks_where': baseObj['geography'],
			}
		except Exception as e:
			print ('BAD balues in baseObj')
			print (baseObj)

		boosts = self.getBoostValues(ks=ks)

		solr = corona()
		# solr_response is a list of objectIds
		try: 
			solr_response = solr.ks_query(queryTerms=queryTerms, boosts=boosts)
		except Exception as e:
			print ('ERROR returned from ks_query')
			print (e)

		
		solr_response['docs'] = self.getImages(solr_response['docs'])
		return solr_response
		
	"""
	Pulls in images from Walters API
	"""

	def getImages(self, objectIds):
		with futures.ThreadPoolExecutor(max_workers=5) as executor:
		    pages = executor.map(self.getObject, objectIds)

		objects = []
		for data in pages:
			obj = {}
			# if for some reason the object could not be returned then ignore and just continue
			if data is None:
				continue
			# get the primary image
			try:
				for image in data['Images']:
					if image['IsPrimary'] is True: obj['imgUrl'] = image['ImageURLs']['Large']	
			except Exception as e:
				print ("EROOR getting images")
				obj['imgUrl'] = ''

			obj['objUrl'] = data['ResourceURL']
			obj['objNumber'] = data['ObjectNumber']
			objects.append(obj)
		# return only data required to print objects
		return {'objects': objects}
	"""
	Turn the text ks values into integers 

	exactly
	prety much
	kinda-sorta
	A little
	not at all

	"""
	def getBoostValues(self, ks):
		# 'not at all' may need some re-thinking
		ks_values = { 
			'exactly': '100', 
			'pretty much': '75', 
			'kinda-sorta': '50', 
			'A little': '25',
			'not at all': '0',
		}
		for key in ks:
			ks[key] = ks_values[ ks[key] ]
		print (ks)
		
		return ks






