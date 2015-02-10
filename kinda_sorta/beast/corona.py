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
		
	stopwords = ['a','an','and','are','as','at','be', 'but', 'by', 'for', 'if', 'in', 'into', 
	'is', 'it', 'no', 'not', 'of', 'on', 'or','such', 'that', 'the', 'their', 'then', 'there', 
	'these', 'they', 'this', 'to', 'was', 'will','with',]
	inst = None

	"""
	"""
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

	"""
	Get a random object out of the index
	"""
	def getRandom(self):
		randNum = str(random.randrange( 500000 ))
		url = self.solrServer + 'select?q=*%3A*&sort=random_' + randNum + '+asc&rows=1&wt=json&indent=true'
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
		
		return json_rsp['response']['docs'][0]['objectId']
		

	"""
	Since I am have zero luck just using straight boosting to change
	my result sets, I think I need to alter the ontology a bit

	Use the word_select() to pull in only a partial term set for each query

	"""
	def ks_query_param(self, qt, b): 
		try:
			toDel = []
			for q in qt:
				if int(b[q]) == 0:
					toDel.append(q)
				else: 
					qt[q] = self.word_select(qt[q], int(b[q]))
			# remove the paramter
			for d in toDel: 
				del qt[d]
			
			return qt
		except Exception as e: 
			print ('Unable to parse params in ks_query_param()')
			print (e)

	"""
	Bulldozed version of what I'd like to encapsulate in a RH or custom 
	Solr code. Adjust the boostings weights and minimum to match dynamically. 

	id: the solrId of the record to build related objects against 

	TODO: remove these 
		id_mat: hard coding paramters to query agaist 
		id_objName: hard coding paramters to query against 

	"""
	def ks_query(self, queryTerms, boosts): 
		# result sets
		results = {'numFound': None, 'docs': []}
		# build query seperately
		queryTerms = self.ks_query_param(qt=queryTerms, b=boosts)

		query = []
		for key in queryTerms:
			query.append('(' + key + ':' + quote_plus(queryTerms[key]) + ')')

		# + '^' + boosts[key]
		url = self.solrServer + 'select?q=+(' + '+'.join(query) + ')&mm=100&fl=score,objectId'
		
		try:
			print (url)
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
			print('Exeption loading response json')
			print (e)
			return None

		# pull object ids out	
		results['numFound'] = json_rsp['response']['numFound']	
		for doc in json_rsp['response']['docs']:
			results['docs'].append(doc['objectId'])

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
		# return the exact phrase b/c that is what they asked for
		if percent == 100: 
			return '"' + words.strip() + '"'

		# remove stop words
		words = ' '.join([word for word in words.split() if word not in self.stopwords])
		
		subString = None
		items = (words.split(' '))

		# if there are less than four words then don't drop anything
		if len(items) < 4:
			return words


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
		








