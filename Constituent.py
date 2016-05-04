#!/usr/bin/python

class Constituent:
	''' 
	A labeled span (start and end pair) representing a constituent tree node.
	Original Java code by Dan Klein.
	'''
	def __init__(self, label, start, end):
		self.label = label
		self.start = start
		self.end = end

	def getLabel(self):
		return self.label

	def getStart(self):
		return self.start

	def getEnd(self):
		return self.end

	def __eq__(self, other):
		if self == other: return True
		if not isinstance(other, Constituent): return False

		if self.end != other.end: return False
		if self.start != other.start: return False
		if self.label is not None and self.label != other.label: return False
		return True

	def __hash__(self):
		result = 0
		if label is not None: result = hash(label)
		result = 29 * result + start
		result = 29 * result + end
		return result
