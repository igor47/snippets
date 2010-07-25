#Unit tests file for highlights
#http://www.yelp.com/search?find_desc=deep+dish+pizza&ns=1&rpp=10&find_loc=San+Francisco%2C+CA

import unittest

class TestHighlights(unittest.TestCase):
	"""Tests the highlights class for to make sure it works"""
	def setUp(self):
		pass

	def testSingle(self):
		"""Make sure that snippets get highlighted"""
		pass

	def testConsecutive(self):
		"""Consecutive highlighted words should be grouped in one highlight"""
		pass

	def testNoMatches(self):
		"""Nothing should be highlighted if the document has no matching groups"""
		pass

class TestExtraction(unittest.testCase):
	"""Tests the ability to exract minimally relevant snippets"""
	def testBasicRelevance(unittest.testCase):
		"""Snippets should be more relevant than non-snippets"""
		pass

	def testSnippetSize(unittest.testCase):
		"""Snippets should be of a certain size and not any longer"""
		pass
