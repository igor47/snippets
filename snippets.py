#!/usr/bin/python
#
# Igor Serebryany
# Yelp Code Test 7/25/09

"""Does the yelp puzzle of snippet highlighting"""
import re

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

	@property
	def bestSnippet(self):
		"""Returns the best snippet"""
		self.buildWordScores()
		return self.findBestSnippet()

	def buildWordScores(self):
		"""Parses out the words in the document and scores them

		The result is a list of dictionaries, one dictionary per word, containing the word's
		'fullword', 'word', 'score' and 'clauseEnder' boolean"""

		wordRe = re.compile(r"[^\s]+\s+")	#this is how we split out words
		clauseIndicators = (',', ';')

		words = []
		bestWordIndex = 0

		for word in wordRe.finditer(self.doc):
			wordInfo = {
					'fullword':word.group(),
					'word':word.group().strip(),
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
			if wordInfo['score'] > words[bestWordIndex]['score']:
				bestWordIndex = len(words) - 1
				print "found new best word '%s' with index %s and score %s" % (wordInfo['word'], bestWordIndex, wordInfo['score'])

		#save the results
		self.words = words
		self.bestWordIndex = bestWordIndex

	def findBestSnippet(self):
		"""Build a snippet around the word with the best score"""
		#figure out where the snippet starts
		minFirstIndex = self.bestWordIndex - self.snippetMaxWords + 1

		#we sacrifice some words from the front of the string to get a sentence-oriented snippet
		for cutFromFront in xrange(self.snippetMaxWords):
			prevWord = self.words[minFirstIndex + cutFromFront - 1]
			curWord = self.words[minFirstIndex + cutFromFront]

			#normally, the score decays by one each word. If the next word has a bigger
			#score than the previous word, it's a matching word and cannot be cut
			if prevWord['score'] < curWord['score']:
				#we try to preceede a matching word by at least minPreceedingWords
				cutFromFront = min(cutFromFront - self.minPreceedingWords, 0)
				break

			#if the prev word is a clause ender, we cut here
			if prevWord['clauseEnder']:
				break

		firstIndex = minFirstIndex + cutFromFront

		#if we have space in our clause, we might could try to find the end of the clause
		lastIndex = self.bestWordIndex + 1
		if cutFromFront == 0:
			for addToEnd in xrange(1, cutFromFront):
				curWord = self.words[self.bestWordIndex + addToEnd]
				if curWord['clauseEnder']:
					break

			lastIndex += addToEnd

		#and now, for the grande finale
		return " ".join([word['word'] for word in self.words[firstIndex:lastIndex]])

def highlightWords(doc, words):
	"""Highlights words in a document
	Args:
		doc -- a string in which to highlight the words
		words -- a string containing the words to highlight

	returns
		A string with the specified words highlighted"""

	return doc

def highlightDoc(doc, query):
	"""Highlights snippets in a document
	Args:
		doc -- document to be highlighted
		query -- the search string

	Returns:
		The most relevant snippets from the document with the search terms highlighted."""

	snipper = Snipper(doc, query)
	return highlightWords(snipper.bestSnippet, query)

