

"""
Cooper-Hewitt 

Reads and stores Cooper-Hewitt collections data into MySQL for indexing to Apache Solr 

Should probably just by-pass MySQL for the time being and dump staright to Solr 
"""

import os
import sys
import scandir
from pprint import pprint
import json
from corona import corona 


class ChBuild():

	def __init__(self):
		pass

	def walk(self, path):
		# traverse root directory, and list directories as dirs and files as files
		solr = corona()
		cnt = 0
		objects = list()
		for root, dirs, files in scandir.walk(path):
			path = root.split('/')
			for file in files:
				if '.json' in file:
					try:
						json_data=open(root + '/' + file).read()
						data = json.loads(json_data)
						doc = {'id': ('ch-' + str(data['tms:id'])), 'objectId': str(data['tms:id']), 'material': self.xstr(data['medium']), 'objectName': self.xstr(data['title']) }
						objects.append( doc )
						if(len(objects) == 25):
							cnt = cnt + 25
							# print (objects)
							solr.add( json.dumps(objects).encode('utf-8') )
							print ('Done with ' + str(cnt))
							del objects[:]
							sys.stdout.flush()
					except Exception as e: 
						print ('Error trying to process file (' + file + ')')
						print (e)
						print (traceback.format_exc())
		# end loop

	"""
	"""
	def xstr(self, string):
		return '' if string is None else string

ch = ChBuild()
ch.walk( os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir, 'data/ch/collection-master/objects/184')) )
