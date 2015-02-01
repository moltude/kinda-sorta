
"""
Class for building out the Objects table
"""

import MySQLdb
import urllib2
import urllib
import json
import pprint
import os

class ObjectsBuild:

	""" 
	DB connection info
	"""
	host='127.0.0.1'
	port=3306
	user='moltude_read'
	passwd=''
	db_name='wam_artbytes'
	db = None
	cursor = None

	"""
	Walters API
	"""
	walters_base_url = 'http://api.thewalters.org/v1/objects'
	walters_api_key=''


	"""
	init
	"""
	def __init__(self):
		self.db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db_name)
		self.cursor = self.db.cursor()

	"""
	del
	"""
	def __del__(self):
		self.db.close()

	"""
	"""
	def query(self, query):
		self.cursor.execute(query)
		data = self.cursor.fetchall()

		if data is not None:
			print "Results for " + query
			for row in data :
				print row[0]
	"""
	Does object record exist in local DB
	returns True/False
	"""
	def exists(self, objectId, repo):
		stmt = "SELECT count(*) FROM Objects WHERE objectId=%s AND repoId=getRepoId('%s')" % (objectId, repo)
		self.cursor.execute(stmt)
		(number_of_rows,)=self.cursor.fetchone()

		if(number_of_rows==0):
			return False
		else: 
			return True

	"""
	Add record to Objects table
	"""
	def addObject(self, objectId, repo) : 
		# If the object does not exist in the Objects table then add it. 
		if(not self.exists(objectId, repo)):
			stmt = "INSERT INTO Objects (objectId, repoId) values (%s, getRepoId('%s'))" % (objectId, repo)
			# Need to add conditional to check if the object already exists in Objects table
			self.cursor.execute(stmt)
			self.db.commit()

	"""
	Queries the Walters API and pulls down all object records 
	Writes to MySQL 

	http://api.thewalters.org/v1/objects?
	"""
	def getAllWalters(self) :
		classifications = [ 'Miniatures','Stained & Painted Glass','Lacquer & Inlay','Ceramics','Precious Stones & Gems','Pearl, Horn, Coral & Shell'
							'Sculpture','Textiles','Painting & Drawing','Prints','Coins & Medals','Arms & Armor','Mosaics & Cosmati','Niello',
							'Paper & Paper-Mache','Wood','Enamels','Manuscripts & Rare Books','Ivory & Bone','Mummies & Cartonnage',
							'Timepieces, Clocks & Watches','Glasswares','Metal','Gold, Silver & Jewelry','Stone','Resin, Wax & Composite','Leather']

		
		# Iterate through all the classifications and get the objectIds for all items
		for classification in classifications:
			print 'Processing ' + classification
			nextPage=True
			page = 1

			while(nextPage):
				nextPage=False;
				url = self.walters_base_url + '?apikey=' + self.walters_api_key + '&Classification='+urllib.quote_plus(classification) + '&page=' + str(page)
				try:
					response = urllib2.urlopen(url)
				except urllib2.HTTPError as e:
					print e
					print 'Unable to open ' + url
					nextPage=False;
				else:
					data = json.load(response)
					items = data['Items']
					for item in items:
						objectId = item['ObjectID']
						self.addObject(objectId, 'The Walters Art Museum')
					nextPage=data['NextPage']
					page=page+1

	"""
	Adds data to local DB
	"""
	def updateFieldContent(self, fields, repository): 
		# select all objects 
		stmt = "SELECT objectId FROM Objects WHERE repoId=getRepoId('%s') and material is null and objectName is null" % (repository)
		self.cursor.execute(stmt)
		data = self.cursor.fetchall()

		obj_cnt = len(data)
		loop_cnt = 1
		for row in data: 
			# logging
			if(loop_cnt % 100 == 0): 
				print '### ' + str(loop_cnt) + '/' + str(obj_cnt)

			content = self.getItem(row[0], fields)

			# if the recrod exists then update
			if(content is not None and self.exists(row[0], repository)):
				stmt = ( 'UPDATE Objects '
					'SET material=%s, '
						'objectName=%s '
					'WHERE objectId=%s '
					'AND repoId=getRepoId(%s) '
					)
				# Need to add conditional to check if the object already exists in Objects table
				# print row[0]
				try:
					self.cursor.execute(stmt, (content['Medium'], content['ObjectName'], row[0], repository))
					self.db.commit()
					print str(row[0])  + ' ' + str(content)
				except (Exception) as e:
					print 'ERROR with SQL update:'
					print stmt
					print e
			loop_cnt += 1


	"""
	Query API and return content of fields requested 
	http://api.thewalters.org/v1/objects/37626
	"""
	def getItem(self, objectId, fields): 
		content = {}
		url = self.walters_base_url + '/' + str(objectId) + '?' + 'apikey=' + self.walters_api_key
		try:
			response = urllib2.urlopen(url)
		except urllib2.HTTPError as e:
			# print e
			print 'Unable to open ' + url
			return None
		data = json.load(response)
		item = data['Data']
		for field in fields: 
			content[field] = item[field]
		return content

	
	"""
	ScrapIt
	Scrape the Walters API and download all object records as json docs 
	Used to perform data analysis and index testing 
	
	"""


"""
Main 
"""
obj = ObjectsBuild()
# obj.query("SELECT objectId From Objects")
# obj.getAllWalters()

# test adding an object that already exists
# obj.addObject(175, 'The Walters Art Museum')

# add material and object name to all Walters objects 
# obj.updateFieldContent(['Medium','ObjectName'] , 'The Walters Art Museum')

# print obj.getItem(37626, ['Medium','ObjectName']))


