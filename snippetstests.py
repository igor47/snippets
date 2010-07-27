#!/usr/bin/python

#Unit tests file for highlights
#http://www.yelp.com/search?find_desc=deep+dish+pizza&ns=1&rpp=10&find_loc=San+Francisco%2C+CA

import unittest, random
import snippets

class TestHighlights(unittest.TestCase):
	"""Tests the highlights class for to make sure it works"""
	def testSingle(self):
		"""Make sure that snippets get highlighted"""
		testCases = (
				{'string':'The quick brown fox jumped over the lazy dog',
					'search':'brown fox'},)
		pass

	def testConsecutive(self):
		"""Consecutive highlighted words should be grouped in one highlight"""
		pass

	def testNoMatches(self):
		"""Nothing should be highlighted if the document has no matching groups"""
		pass

class TestExtraction(unittest.TestCase):
	"""Tests the ability to exract minimally relevant snippets"""
	@classmethod
	def setUpClass(cls):
		cls.commandline = open('commandline.txt').read()

	def testNoMatchReturnsBeginning(self):
		"""Searching for words not in the document should return the beginning of the document"""
		s = snippets.Snipper(self.commandline, 'asteroid cherry')
		s.snippetMaxWords = 10
		snippet = s.bestSnippet
		self.assertEqual(snippet, 'In the Beginning was the Command Line\r\n\r\nby Neal Stephenson')

	def testBasicRelevance(self):
		"""Snippets should be more relevant than non-snippets"""
		doc = "This is an irrelevant sentence. This is a filler sentence. This is a relevant sentence.";
		s = snippets.Snipper(doc, 'relevant')
		s.snippetMaxWords = 5
		self.assertEqual(s.bestSnippet, "This is a relevant sentence.")

	def testSnippetSize(self):
		"""Snippets should be of a certain size and not any longer"""
		testSearches = ('car wind', 'emacs', 'dolphins', 'control freak', 'making your own')
		for search in testSearches:
			s = snippets.Snipper(self.commandline, search)
			maxSize = random.randRange(20, 150)

			s.snippetMaxWords = maxSize
			self.assertLessEqual(len(s.bestSnippet), maxsize, 'Snippet too large when searching for %s with maxSize %d' % (search, maxSize))

def suite():
	extractionSuite = unittest.defaultTestLoader.loadTestsFromTestCase(TestExtraction)
	highlightSuite = unittest.defaultTestLoader.loadTestsFromTestCase(TestHighlights)

	allTests = unittest.TestSuite((extractionSuite, highlightSuite))
	return allTests

if __name__ == "__main__":
	allTests = suite()
	unittest.TextTestRunner(verbosity=2).run(allTests)
