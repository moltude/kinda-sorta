"""
Class for moving data to Solr 
"""
from django.conf import settings
from urllib.parse import quote_plus

import platform
import urllib
import string
import json
import urllib.request
import numpy as np
import random
import string
import os 

class corona:

	# TODO pull from Heroku ENV var
	HEROKU = bool(os.environ.get('ON_HEROKU', ''))
	if HEROKU:
		solrServer = os.environ['SOLR_EC2']
	if not HEROKU:
		try:
			solrServer = settings.SOLR_EC2
			# if unable to load from settings file then just hard coded
		except Exception as e:
			print(e)
		

	inst = None
	def __init__(self): 
		pass

	def ping (self):
		url = self.solrServer + "select?q=*%3A*&wt=json&indent=true"
		try:
			f = urllib.request.urlopen(url)
			if f.getcode() == 200:
				return True
			else:
				print (req)
				return False
		except Exception as e:
			print (e)
			print (req.encode('utf-8'))
	"""
	Delete all the content from Solr 
	"""
	def deleteAll(self):
		deleteRequest = self.solrServer + 'update?stream.body=%3Cdelete%3E%3Cquery%3E*:*%3C/query%3E%3C/delete%3E&commit=true'
		pass
	"""
	"""
	def add(self, doc):
		req = urllib.request.Request(url=self.solrServer+'/update/json?commit=true', data=doc)
		req.add_header('Content-type', 'application/json')
		try:
			f = urllib.request.urlopen(req)
			if f.getcode() == 200:
				return True
			else:
				print (req)
				return False
		except Exception as e:
			print (e)
			print (req.encode('utf-8'))
		
		## Begin using data like the following

	"""
	Bulldozed version of what I'd like to encapsulate in a RH or custom 
	Solr code. Adjust the boostings weights and minimum to match dynamically. 

	id: the solrId of the record to build related objects against 

	TODO: remove these 
		id_mat: hard coding paramters to query agaist 
		id_objName: hard coding paramters to query against 

	"""
	def ks_query(self, queryTerms, boosts): 
		results = []

		# TODO :: move some of these parameters into the 
		# /select request handler
		url = self.solrServer + 'select?q='\
		+ 'ks_how:'+ queryTerms['ks_how'] \
		+ ' OR ks_what:' + queryTerms['ks_what'] \
		+ ' OR ks_who:' + queryTerms['ks_who'] \
		+ ' OR ks_where:' + queryTerms['ks_where']

		# comment out the boosts until implementation
		# + '&qf=ks_how^' + boosts['ks_how'] \
		# + '&qf=ks_what^' + boosts['ks_what'] \
		
		print ("QUERY URL= " + url)
		
		try:
			response = urllib.request.urlopen(url)
		except Exception as e: 
			print ('Exception thrown fetching from Solr')
			print (url)
			# TODO :: Some stock query behavior and messaging so they get some results 
			print (e)
			return None

		try:
			json_rsp = json.loads(response.read().decode("utf-8"))
		except Exception as e:
			print (e)
			print('Exeption loading response json')
			return None

		# pull object ids out		
		for doc in json_rsp['response']['docs']:
			results.append(doc['objectId'])

		# The response from Solr should only the the ObjectIDs because I will need to requery for all 
		# items to get images from Walters API
		return results

	"""
	select?q=*%3A*&wt=json&indent=true
	"""
	def query(self, q): 
		url = self.solrServer + '/select?q=*%3A*&wt=json&indent=true'
		result = urllib.request.urlopen('http://localhost:8983/solr/kinda-sorta/select?q=*%3A*&wt=json&indent=true').read()

	def word_select(self, words, percent): 
		words = self.clean_words(words)
		subString = None
		items = (words.split(' '))

		t_sub = int(float((percent/100.0))*len(items))

		# pick an item index
		for x in range(0, t_sub):
			if subString is None:
				subString = ''
			index = random.randrange( len(items) )
			subString = subString + ' ' + items.pop(index)

		if subString is None: 
			return '*'
		else:
			return subString.strip()

	def clean_words(self, words): 
		exclude = set(string.punctuation)
		table = string.maketrans("","")
		return words.translate(table, string.punctuation)


"""
Testing blocks 
# """
# solr = corona()

# print (platform.python_version())

# quit()

# material = 'black chalk, brush and brown wash, incised lines and compass points on cream laid paper, lined'
# objectName = 'DRAWING, DESIGN FOR A CANDLESTICK, 1520-30'

# for mat_weight in np.arange(100.0, 0.0, -10):
# 	for objName_weight in np.arange(0.0, 100.0, 10):
# 		m = solr.word_select(material, mat_weight)
# 		o = solr.word_select(objectName, objName_weight)

# 		# debug
# 		print ('mat_weight: ' + str(mat_weight) + ' for: ' + m)
# 		print ('objName_weight: ' + str(objName_weight) + ' for: ' + o)

# 		print		

# 		result = solr.ks_query(
# 			id=None, 
# 			mq=m,
# 			oq=o,
# 			mat_weight=mat_weight, 
# 			mat_mm=mat_weight, 
# 			objName_weight=objName_weight, 
# 			objName_mm=None)
# 		# print str(result)
# 		print 
# 		print 
		








