#!/usr/bin/python

#Unit tests file for highlights
#http://www.yelp.com/search?find_desc=deep+dish+pizza&ns=1&rpp=10&find_loc=San+Francisco%2C+CA

import unittest
import snippets

class TestHighlights(unittest.TestCase):
	"""Tests the highlights class for to make sure it works"""
	def testSingle(self):
		"""Make sure that snippets get highlighted"""
		testCases = (
				{
					'string'=>'The quick brown fox jumped over the lazy dog',
					'search'=>'brown fox'}

	def testConsecutive(self):
		"""Consecutive highlighted words should be grouped in one highlight"""
		pass

	def testNoMatches(self):
		"""Nothing should be highlighted if the document has no matching groups"""
		pass

class TestExtraction(unittest.testCase):
	"""Tests the ability to exract minimally relevant snippets"""
	@classmethod
	def setUpClass(self):
		self.commandline = open('commandline.txt').read()

	def testNoMatchReturnsBeginning(unittest.testCase):
		"""Searching for words not in the document should return the beginning of the document"""
		s = snippets.Snipper(self.commandline, 'asteroid cherry')
		s.
		snippet = s.bestSnippet
		self.assertEqual(snippet[0:


	def testBasicRelevance(unittest.testCase):
		"""Snippets should be more relevant than non-snippets"""
		

	def testSnippetSize(unittest.testCase):
		"""Snippets should be of a certain size and not any longer"""
		pass

def suite():
	extractionSuite = unittest.defaultTestLoader.loadTestsFromTestCase(TextExtraction)
	highlightSuite = unittest.defaultTestLoader.loadTestsFromTestCase(TestHighlights)

	allTests = unittest.TestSuite((extractionSuite, highlightSuite))
	return allTests

if __name__ == "__main__":
	allTests = suite()
	unittest.TextTestRunner(verbosity=2).run(allTests)
