"""
Validate input from users into search form 
"""


from urllib.parse import urlparse
import re

class v:
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
				print ("("+c1+")"+"("+word1+")"+"("+c2+")"+"("+int1+")")
				t = int1
		except Exception as e:
			print ('Exception thrown in get_objectId()' )
			print (e)
			return None
		# return on success
		if (t == ''):
			print ('t is blank')
			return None

		print ('RETURNING ' + t)
		return str(t)

	"""
	"""
	def is_number(self, s):
		try:
			float(s)
			return True
		except ValueError:
			return False

url='http://art.thewalters.org/detail/32876/albarello-with-a-shepherdess-lifting-her-skirt/?type=date&letter=a&sort=title&order=asc&begin_date=-10000&end_date=2015'

g = ''
val = v()
g = val.get_objectId(url)

print (g)

print (val.is_number(g))