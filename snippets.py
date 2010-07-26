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
	This is organized as an object so that individual sections can be more easily replaced,
	and so that internal state can be concealed someplace

	This assumes that documents will be real english prose text -- it will not do well with
	extensive math or strange characters"""

	snippetMaxWords = 60		#at most this many words
	snippetMinWords = 30		#at least this many words
	minPreceedingWords = 5	#first match must have at least this many words ahead 
	                      	#of it, but not more than snippetMaxWords

	def __init__(self, doc, query):
		self.doc = doc
		self.query = query

		self.queryWords = self.query.split()

		self.words = []
		self.bestWordIndex = None
		self.bestSnippet = None

	@property
	def bestSnippet(self):
		"""Returns the best snippet"""
		self.buildWordScores()
		self.findBestSnippet()

		return self.bestSnippet

	def buildWordList(self):
		"""Parses out the words in the document and puts them into a list"""
		wordRe = re.compile(r"[^\s]+\s+")	#this is how we split out words
		clauseIndicators = (',', ';')

		words = []
		maxWordIndex = 0

		for word in wordRe.finditer(self.doc):
			wordInfo = {
					'fullword':word,
					'word':word.strip(),
					'clauseEnder':False,
					}

			#determine if this ends a clause -- useful for building the snippet
			for indicator in clauseIndicators:
				if wordInfo['word'].endswith(indicator):
					wordInfo['clauseEnder'] = True

			#determine the score for this word
			wordInfo['score'] = -1	#non-matching words decay store by 1
			for queryWord in self.queryWords:
				if wordInfo['word'].startswith(queryWord):
					#Matching words jump the score by the snippet size
					#This allows us to keep track of density in the snippet
					wordInfo['score'] = self.snippetMaxWords

			#combine with preceeding word to form score so far
			if len(words) > 0:
				#score never drops below 0
				wordInfo['score'] = max(wordInfo['score'] + words[-1]['score'], 0)

			words.append(wordInfo)

			#are we now the bestest word?
			if wordInfo['score'] > words[maxWordIndex]['score']:
				maxWordIndex = len(words) - 1

		#save the results
		self.words = words
		self.maxWordIndex = maxWordIndex

	def findBestSnippet(self):
		"""Build a snippet around the word with the best score"""
		half = self.snippetMaxWords/2

		#figure out where the snippet starts
		minFirstIndex = self.bestWordIndex - self.snippetMaxWords

		#we sacrifice some words from the front of the string to get a sentence-oriented snippet
		sentenceFirst = None
		for cutFromFront in xrange(half):
			prevWord = self.words[minFirstIndex + cutFromFront - 1]
			currentWord = self.words[minFirstIndex + cutFromFront]

			#normally, the score decays by one each word. If the next word has a bigger
			#score than the previous word, it's a matching word and cannot be cut
			if prevWord['score'] < currentWord['score']:
				#we try to preceede a matching word by at least minPreceedingWords
				cutFromFront = min(cutFromFront - minPreceedingWords, 0)
				break

			#if the prev word is a clause ender, we cut here
			if prevWord['clauseEnder']:
				break

		firstIndex = minFirstIndex + cutFromFront

		#if we have space in our clause, we might could try to find the end of the clause
		if cutFromFront == 0:
			lastIndex = self.bestWordIndex

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

