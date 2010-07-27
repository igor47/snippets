#!/usr/bin/python

#Unit tests file for highlights
#http://www.yelp.com/search?find_desc=deep+dish+pizza&ns=1&rpp=10&find_loc=San+Francisco%2C+CA

import unittest, random
import snippets

class TestHighlights(unittest.TestCase):
	"""Tests the highlights class for to make sure it works"""
	def testSingle(self):
		"""Make sure that words get highlighted"""
		doc = "The quick brown fox jumped over a lazy dog."

		s = snippets.Snipper(doc, 'the', maxWords = 200)
		self.assertEqual(
				s.bestSnippetHighlighted,
				"[[HIGHLIGHT]]The[[ENDHIGHLIGHT]] quick brown fox jumped over a lazy dog.")

		s = snippets.Snipper(doc, 'fox', maxWords = 200)
		self.assertEqual(
				s.bestSnippetHighlighted,
				"The quick brown [[HIGHLIGHT]]fox[[ENDHIGHLIGHT]] jumped over a lazy dog.")

		s = snippets.Snipper(doc, 'dog', maxWords = 200)
		self.assertEqual(
				s.bestSnippetHighlighted,
				"The quick brown fox jumped over a lazy [[HIGHLIGHT]]dog[[ENDHIGHLIGHT]].")

	def testConsecutive(self):
		"""Consecutive highlighted words should be grouped in one highlight"""
		doc = "The quick brown fox jumped over a lazy dog."

		s = snippets.Snipper(doc, 'brown fox', maxWords = 200)
		self.assertEqual(
				s.bestSnippetHighlighted,
				"The quick [[HIGHLIGHT]]brown fox[[ENDHIGHLIGHT]] jumped over a lazy dog.")

		s = snippets.Snipper(doc, 'dog brown fox lazy', maxWords = 200)
		self.assertEqual(
				s.bestSnippetHighlighted,
				"The quick [[HIGHLIGHT]]brown fox[[ENDHIGHLIGHT]] jumped over a [[HIGHLIGHT]]lazy dog[[ENDHIGHLIGHT]].")

		s = snippets.Snipper(doc, 'the quick brown fox over a lazy dog', maxWords = 200)
		self.assertEqual(
				s.bestSnippetHighlighted,
				"[[HIGHLIGHT]]The quick brown fox[[ENDHIGHLIGHT]] jumped [[HIGHLIGHT]]over a lazy dog[[ENDHIGHLIGHT]].")

		s = snippets.Snipper(doc, 'the quick brown fox jumped over a lazy dog', maxWords = 200)
		self.assertEqual(
				s.bestSnippetHighlighted,
				"[[HIGHLIGHT]]The quick brown fox jumped over a lazy dog[[ENDHIGHLIGHT]].")

	def testNoMatches(self):
		"""Nothing should be highlighted if the document has no matching groups"""
		pass

class TestExtraction(unittest.TestCase):
	"""Tests the ability to exract minimally relevant snippets"""
	def testSizeOneSnippetsWithMatch(self):
		"""Size one snippets should just return the match"""
		doc = 'in the beginning was the command line'
		for searchString in ('in', 'was', 'line'):
			s = snippets.Snipper(doc, searchString, maxWords = 1)
			self.assertEqual(s.bestSnippet, searchString)

	def testSnippetSize(self):
		"""Snippets should be of a certain size and not any longer"""
		commandline = open('command.txt').read()
		searchStrings = ('car wind', 'asteroid cherry', 'control freak', 'making your own')

		#build a list of sizes to test
		maxSizes = [2, 3, 10, 100, 1000]

		for search in searchStrings:
			for size in maxSizes:
				s = snippets.Snipper(commandline, search, maxWords = size)
				self.assertTrue(len(s.getBestSnippetWords()) <= size)

	def testNoMatchReturnsBeginning(self):
		"""Searching for words not in the document should return the beginning of the document"""
		s = snippets.Snipper("There are no such words here", 'asteroid cherry')

		s.maxWords = 1
		self.assertEqual(s.bestSnippet, "There")

		s.maxWords = 2
		self.assertEqual(s.bestSnippet, "There are")

		s.maxWords = 3
		self.assertEqual(s.bestSnippet, "There are no")

		s.maxWords = 50
		self.assertEqual(s.bestSnippet, "There are no such words here")

	def testSentenceRounding(self):
		"""We should round to the nearest clause both ahead and in front"""
		doc = "This is an irrelevant sentence. This is a filler sentence. This is a relevant sentence.";

		s = snippets.Snipper(doc, 'relevant', maxWords = 6)
		self.assertEqual(s.bestSnippet, "This is a relevant sentence.")

		s = snippets.Snipper(doc, 'relevant', maxWords = 4)
		self.assertEqual(s.bestSnippet, "This is a relevant")

		s = snippets.Snipper(doc, 'relevant', maxWords = 3)
		self.assertEqual(s.bestSnippet, "is a relevant")

		#ideally, the last test would result in 'a relevant sentence.'
		#it does not because we cut all the words before 'relevant' but then we can't
		#append all those words to the end because we run out of document. to add the
		#'a' back in, we'd have to see how much of the cut space we used and then re-add
		#the leftovers back to the beginning
		s = snippets.Snipper(doc, 'relevant', maxWords = 3, minPreceedingWords = 0)
		self.assertEqual(s.bestSnippet, "relevant sentence.")

def suite():
	extractionSuite = unittest.defaultTestLoader.loadTestsFromTestCase(TestExtraction)
	highlightSuite = unittest.defaultTestLoader.loadTestsFromTestCase(TestHighlights)

	allTests = unittest.TestSuite((extractionSuite, highlightSuite))
	return allTests

if __name__ == "__main__":
	allTests = suite()
	unittest.TextTestRunner(verbosity=0).run(allTests)
