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

		self.bestWordIndex = None

	@property
	def bestSnippet(self):
		"""Returns the best snippet"""
		bestSnippetWords = self.getBestSnippetWords()
		return "".join([word['fullword'] for word in bestSnippetWords]).strip()

	@property
	def bestSnippetHighlighted(self):
		"""Returns the best snippet with the matches highlighted"""
		bestSnippetWords = self.getBestSnippetWords()
		return self.highlightSnippet(bestSnippetWords)

	def getBestSnippetWords(self):
		"""Returns the word list of the words in the best snippet"""
		queryWords = self.buildQueryWordList(self.query)
		documentWords, bestWordIndex = self.buildWordScores(self.doc, queryWords)
		bestSnippetWords = self.findBestSnippet(documentWords, bestWordIndex)

		return bestSnippetWords

	def buildWordScores(self, document, queryWords):
		"""Parses out the words in the document and scores them
		args:
			doc -- the document from which words are extracted
			queryWords -- a list of words which are scored highly

		The result is a list of dictionaries, one dictionary per word,
		containing the word, it's full expression, it's trail, score and
		booleans for whether it is a clause ender or matches a query word"""

		wordRe = re.compile(r"""([a-z0-9'`"]+)([^a-z0-9'`"]+)""", re.IGNORECASE)	#this is how we split out words
		clauseIndicators = ('.', ';')

		words = []
		bestWordIndex = 0

		for word in wordRe.finditer(document):
			wordInfo = {
					'fullword':word.group(0),
					'word':word.group(1),
					'trail':word.group(2),
					'matching':False,
					'score':-1,		#non-matching words decay score by 1
					'clauseEnder':False,
					}

			#determine if this ends a clause -- useful for building the snippet
			for indicator in clauseIndicators:
				if wordInfo['trail'].startswith(indicator):
					wordInfo['clauseEnder'] = True

			#determine the score for this word
			for queryWord in queryWords:
				if queryWord == wordInfo['word']:
					wordInfo['matching'] = True
					#matching words jump score by the snippet size
					wordInfo['score'] = self.snippetMaxWords

			#combine with preceeding word to form score so far
			if len(words) > 0:
				wordInfo['score'] = max(wordInfo['score'] + words[-1]['score'], 0)
			else:
				wordInfo['score'] = 1		#give some weight to the start of document

			#we want to eliminate the influence of words which don't even make it into this window
			currentIndex = len(words)
			lastOutOfWindow = currentIndex - self.snippetMaxWords
			if lastOutOfWindow >= 0:
				wordInfo['score'] = max(wordInfo['score'] - words[lastOutOfWindow]['score'], 0)

			words.append(wordInfo)

			#are we now the bestest word?
			if wordInfo['score'] > words[bestWordIndex]['score']:
				bestWordIndex = currentIndex

		#and vioala!
		return words, bestWordIndex

	def findBestSnippet(self, words, bestWordIndex):
		"""Build a snippet around the word with the best score"""
		#figure out where the snippet starts
		if bestWordIndex > self.snippetMaxWords:
			minFirstIndex = bestWordIndex - self.snippetMaxWords + 1

			#we might be able to  sacrifice some words from the front of the string
			#To get a clause start at the front and back
			for cutFromFront in xrange(self.snippetMaxWords):
				prevWord = words[minFirstIndex + cutFromFront - 1]
				curWord = words[minFirstIndex + cutFromFront]

				#normally, the score decays by one each word. If the next word has a bigger
				#score than the previous word, it's a matching word and cannot be cut
				if prevWord['score'] < curWord['score']:
					#we try to preceede a matching word by at least minPreceedingWords
					cutFromFront = max(cutFromFront - self.minPreceedingWords, 0)
					break

				#if the prev word is a clause ender, we cut here
				if prevWord['clauseEnder']:
					break

			firstIndex = minFirstIndex + cutFromFront + 1	#off by one fixer
		else:
			firstIndex = 0		#we start at the beginning of the document
			cutFromFront = self.snippetMaxWords - bestWordIndex

		#if we have space in our clause, we might could try to find the end of the clause
		lastIndex = bestWordIndex + 1
		if cutFromFront > 0:
			for addToEnd in xrange(1, cutFromFront):
				curWord = words[bestWordIndex + addToEnd]
				if curWord['clauseEnder']:
					break

			lastIndex += addToEnd

		#and now, for the grande finale
		return words[firstIndex:lastIndex]

	def buildQueryWordList(self, query):
		"""Builds a list of matching words from the query string

		we use a basic stemming algorithm which isn't very sophisicated
		but should be better than nothing"""
		import words

		suffixes = ['s', 'ing', 'est', 'ed', 'er', 'dom', 'like', 'ish', 'ly', 'ness', 'y', 'ism']
		queryWords = query.split()
		baseWords = []
		finalWords = []

		for queryWord in queryWords:
			if queryWord in words.words:
				baseWords.append(queryWord)

				for suffix in suffixes:
					if queryWord.endswith(suffix):
						baseWord = queryWord[0:queryWord.rfind(suffix)]
						if baseWord in words.words:
							baseWords.append(baseWord)

			#always keep the query word	
			else:
				finalWords.append(queryWord)

		for baseWord in baseWords:
			for suffix in suffixes:
				finalWord = baseWord + suffix
				if finalWord in words.words:
					finalWords.append(finalWord)

			#always keep the base word
			finalWords.append(baseWord)

		#we may have gotten dupes when we saved the queryWord AND a finalWord
		finalWords = list(set(finalWords))
		return finalWords

	def highlightSnippet(self, snippetWords):
		"""Highlights words in a document
		Args:
			snippetWords -- a list of words which comprise the snippet (from buildWordScores)
		returns
			A string with the matching words from the query highlighted"""

		highlightedSnippet = ""
		alreadyHighlighting = False

		for index in xrange(len(snippetWords)):
			snippetWord = snippetWords[index]
			if snippetWord['matching'] and not alreadyHighlighting:
				highlightedSnippet += "[[HIGHLIGHT]]"
				alreadyHighlighting = True

			highlightedSnippet += snippetWord['word']

			if alreadyHighlighting:
				try:
					nextWord = snippetWords[index + 1]
				except IndexError:
					nextWord = None

				if not nextWord or not nextWord['matching']:
					highlightedSnippet += "[[ENDHIGHLIGHT]]"
					alreadyHighlighting = False

			highlightedSnippet += snippetWord['trail']

		return highlightedSnippet.strip()

def highlightDoc(doc, query):
	"""Highlights snippets in a document
	Args:
		doc -- document to be highlighted
		query -- the search string

	Returns:
		The most relevant snippets from the document with the search terms highlighted."""

	snipper = Snipper(doc, query)
	return snipper.bestSnippetHighlighted()
