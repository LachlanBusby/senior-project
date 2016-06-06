from collections import defaultdict

"""
DEPRECATED. Using NLTK libraries now.
See pseudo_parser, stmt_parser and stmt_classifier.
"""

class Lexicon:
	'''Simple default implementation of a lexicon, which scores word,
	tag pairs with a smoothed estimate of P(tag|word)/P(tag).'''

	# Builds a lexicon from the observed tags in a list of training trees.
	def __init__(self, trainTrees):
		self.wordToTagCounters = defaultdict(float)
		self.totalTokens = 0.0
		self.totalWordTypes = 0.0
		self.tagCounter = defaultdict(float)
		self.wordCounter = defaultdict(float)
		self.typeTagCounter = defaultdict(float)

		for trainTree in trainTrees:
			words = trainTree.getYield()
			tags = trainTree.getPreTerminalYield()
			for position in xrange(len(words)):
				word = words[position]
				tag = tag[position]
				self.tallyTagging(word, tag)

	def tallyTagging(self, word, tag):
		if not self.isKnown(word):
			self.totalWordTypes += 1
			self.typeTagCounter[tag] += 1

		self.totalTokens += 1
		self.tagCounter[tag] += 1
		self.wordCounter[word] += 1
		self.wordToTagCounters[(word, tag)] += 1

	def isKnown(self, word):
		return word in self.wordCounter.keys()

	def getAllTags(self):
		return tagCounter.keys()

	# Returns a smoothed estimate of P(word|tag)
	def scoreTagging(self, word, tag):
		p_tag = self.tagCounter[tag] / self.totalTokens
		c_word = self.wordCounter[word]
		c_tag_and_word = self.wordToTagCounters[(word, tag)]
		if c_word < 10: # rare or unknown
			c_word += 1
			c_tag_and_word += self.typeTagCounter[tag] / self.totalWordTypes

		p_word = (1.0 + c_word) / (self.totalTokens + self.totalWordTypes)
		p_tag_given_word = c_tag_and_word / c_word
		return p_tag_given_word / p_tag * p_word
