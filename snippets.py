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

	def __init__(self, doc, query, maxWords = 60, minPreceedingWords = 5):
		self.doc = doc
		self.query = query

		self._maxWords = maxWords
		self._minPreceedingWords = minPreceedingWords

	@property
	def maxWords(self):
		"""At most this many words in the snippet"""
		return self._maxWords

	@maxWords.setter
	def maxWords(self, value):
		"""We need at least 1 word in the snippet"""
		if value < 1:
			raise ValueError("Need at least 1 word in the snippet")
		self._maxWords = value

	@property
	def minPreceedingWords(self):
		"""At least this many words before the first match"""
		return self._minPreceedingWords

	@minPreceedingWords.setter
	def minPreceedingWords(self, value):
		if value < 0:
			raise ValueError("Cannot have negative preceeding words")
		return self._minPreceedingWords

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

		wordRe = re.compile(r"""([a-z0-9'`"]+)([^a-z0-9'`"]+|$)""", re.IGNORECASE)	#this is how we split out words
		clauseIndicators = ('.', ';')

		words = []
		bestWordIndex = 0

		for word in wordRe.finditer(document):
			wordInfo = {
					'fullword':word.group(0),
					'word':word.group(1).lower(),
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
					wordInfo['score'] = self.maxWords

			#combine with preceeding word to form score so far
			if len(words) > 0:
				wordInfo['score'] = max(wordInfo['score'] + words[-1]['score'], 0)
			else:
				wordInfo['score'] = 0

			#we want to eliminate the influence of words which don't even make it into this window
			currentIndex = len(words)
			lastOutOfWindow = currentIndex - self.maxWords
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
		#we always add one to bestWordIndex because we want this item to make it into the slicing
		bestWordIndex += 1
		#figure out where the snippet starts
		if bestWordIndex  > self.maxWords:
			minFirstIndex = bestWordIndex - self.maxWords

			#we might be able to  sacrifice some words from the front of the string
			#to get a clause start at the front of the snippet
			for cutFromFront in xrange(self.maxWords):
				prevWord = words[minFirstIndex + cutFromFront - 1]
				curWord = words[minFirstIndex + cutFromFront]

				#normally, the score decays by one each word. If the next word has a bigger
				#score than the previous word, it's a matching word and cannot be cut
				if prevWord['score'] < curWord['score']:
					break

				#if the prev word is a clause ender, we cut here
				if prevWord['clauseEnder']:
					break

			firstIndex = minFirstIndex + cutFromFront

			#if we didn't find the beginning of the clause, we want to give a bit of a buffer
			#to the best word. Try to give at least minPreceedingWords unless that puts the
			#snippet over maxWords
			if not prevWord['clauseEnder']:
				preceedingWords = bestWordIndex - firstIndex
				if cutFromFront > 0 and preceedingWords < self.minPreceedingWords:
					neededWords = self.minPreceedingWords - preceedingWords

					if neededWords > cutFromFront:
						#we need more words than we've cut -- just undo the cutting
						firstIndex -= cutFromFront
						cutFromFront = 0
					else:
						#we cut more words that we need -- undo some of the cutting
						firstIndex -= neededWords
						cutFromFront -= neededWords
		else:
			firstIndex = 0		#we start at the beginning of the document
			cutFromFront = self.maxWords - bestWordIndex

		#if we have space in our snippet, we might could try to find the end of the clause
		lastIndex = bestWordIndex
		if cutFromFront > 0:
			try:
				for addToEnd in xrange(1, cutFromFront + 1):
					curWord = words[lastIndex + addToEnd]
					if curWord['clauseEnder']:
						break
			except IndexError:
				pass			#ran out of words

			lastIndex = lastIndex + addToEnd

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
		finalWords = [word.lower() for word in set(finalWords)]
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
