"""
Class for moving data to Solr 
"""
from django.conf import settings

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
		solrServer = settings.SOLR_EC2

	solrServer = settings.SOLR_EC2

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
		deleteRequest = 'http://localhost:8983/solr/kinda-sorta/update?stream.body=%3Cdelete%3E%3Cquery%3E*:*%3C/query%3E%3C/delete%3E&commit=true'
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
		

	"""
	http://localhost:8983/solr/kinda-sorta/select?q=*%3A*&wt=json&indent=true
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
		








