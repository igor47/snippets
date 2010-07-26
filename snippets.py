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
	This is organized as an object so that individual sections can be more easily replace
	This assumes that documents will be real english prose text -- it will not do well with
	extensive math or strange characters"""

	snippetClauses = 3
	snippetMaxWords = 60
	snippetMinWords = 30

	def __init__(self, doc, query):
		self.doc = doc
		self.query = query

		self.queryWords = self.query.split()

	def buildWordScores(self):
		"""Parses out the words in the document and scores them

		the self.words list will contain a list of dictionaries containing a word, it's score, and
		whether the word is a clause ender"""

		wordRe = re.compile(r"[^\s]+\s+")	#this is how we split out words
		clauseIndicators = (',', ';')

		words = []
		maxWordIndex = 0

		for word in wordRe.finditer(self.doc):
			wordInfo = {
					'fullword':word,
					'word':word.strip(),
					'clauseEnd:False,
					'score':-1,
					}

			#determine if this ends a clause -- useful for building the snippet
			for indicator in clauseIndicators:
				if wordInfo['word'].endswith(indicator):
					wordInfo['clauseEnd'] = True

			#determine the score for this word
			for queryWord in self.queryWords:
				if wordInfo['word'].startswith(queryWord):
					wordInfo['score'] = 1

			#combine with preceeding word to form score so far
			if len(words) > 0:
				wordInfo['score'] += words[-1]['score']

			words.append(wordInfo)

			#are we now the bestest word?
			if wordInfo['score'] > words[maxWordIndex]['score']:
				maxWordIndex = len(words) - 1

		#save the results
		self.words = words
		self.maxWordIndex = maxWordIndex

	def findBestSnippet(self):
		"""Build a snippet around the word with the best score"""
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

