#!/usr/bin/python
#
# Igor Serebryany
# Yelp Code Test 7/25/09

"""Does the yelp puzzle of snippet highlighting"""

def highlightDoc(doc, query):
	"""Highlights snippets in a document
	Args:
		doc -- document to be highlighted
		query -- the search string

	Returns:
		The most relevant snippets from the document with the search terms highlighted."""

	return ""

class Snipper(object):
	"""An object that extracts and highlights snippets in documents
	This is organized as an object so that individual sections can be more easily replace"""
	snippetSize = 3		#in sentences
	def __init__(self, doc, query):
		self.doc = doc
		self.query = query

		self.queryWords = self.query.split()
	
	def findSnippets(self):
		#this is a state machine
		#we slide along the document, keeping a window of at most snippetSize
		#we slide one sentence at a time
		#for every window, we evaluate it's relevance and 

	def sentenceIterator(self):
		"""This iterator yields sentences from the document, one at a time"""
		pass

	def sentenceWeight(self):
		pass

def mostRelevantSnippet(doc, query):
	"""Finds the most relevant snippet in a document
	Args:
		doc -- the document
		query -- the string containing the query

	returns:
		the string with the most relevant snippet"""

	return ""

def highlightWords(doc, words):
	"""Highlights words in a document"""
	pass

