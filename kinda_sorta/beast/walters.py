

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

class walters():

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
	"""
	def flatten(self, data): 
		creators = '' 
		# creators Creators 
		if 'Creators' in data: 
			numCreators = len(data['Creators'])
			for numCreators, creator in enumerate(data['Creators']):
				if numCreators == len(data['Creators']):
					creators = creators + ' and ' + creator['ConcatDisplayName']
				elif numCreators > 1:
					creators = creators + ', ' + creator['ConcatDisplayName']
				else: 
					creators = creator['ConcatDisplayName']
			data['Creators'] = creators

		return data


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




