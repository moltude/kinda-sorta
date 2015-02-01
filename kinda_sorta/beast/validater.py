"""
Validate input from users into search form 

The first iteration only accepts Walters URLs

"""
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re

class validater (): 
	"""
	The public method for validating a URL 
	Takes the string submitted by the user
	"""
	def validate(self, url): 
		# First check -- syntax -- does it look like a URL?
		if (not self.syntax(url)):
			raise Exception('not valid syntax')
		if (not self.is_walters(url)):
			raise Exception('is not from the Walters')
		objectId = (self.get_objectId(url))
		if (objectId == None):
			raise Exception('could not find objectId')
		return objectId

	"""
	Is the URL Walters?
	"""
	def is_walters(self, url):
		try:
			o = urlparse(url)
		except Exception as e:
			return False
		# is this the correct domain?
		if(o[1] != 'art.thewalters.org'):
			print (o[1])
			return False
		else:
			return True
	"""
	Get the objectId from the URL
	"""
	def get_objectId(self, url):
		t = ''
		try:
			# copied from txt2re 
			re1='(\\/)'	# Any Single Character 1
			re2='(detail)'	# Word 1
			re3='(\\/)'	# Any Single Character 2
			re4='(\\d+)'	# Integer Number 1

			rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
			m = rg.search(url)
			if m:
				c1=m.group(1)
				word1=m.group(2)
				c2=m.group(3)
				int1=m.group(4)
				t = int1
		except Exception as e:
			return None
		# return on success
		if (t == ''):
			return None

		return str(t)


	"""
	Checks the submission for formatting 
	"""
	def syntax (self, url):
		val = URLValidator()
		try:
			# if no issues then return true
			val(url)
		except:
			return False
		return True
