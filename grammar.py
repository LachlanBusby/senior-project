import sys

class Grammar():

	class BinaryRule():
		""" A binary grammar rule with score representing its probability. """

		def __init__(self, parent, left_child, right_child):
			self.parent = parent
			self.leftChild = left_child
			self.rightChild = right_child

		def getParent(self):
			return self.parent

		def getLeftChild(self):
			return self.leftChild

		def getRightChild(self):
			return self.rightChild

		def getScore(self):
			return self.score

		def setScore(self, score):
			self.score = score

		def toString(self):
			return self.parent + "->" + self.leftChild + " " + self.rightChild + " %% " + self.score

		def __eq__(self, other):
			return False if not isinstance(other, self.__class__)
			
			if self.parent == None:
				return False if other.parent != None
			else:
				return False if self.parent != other.parent
			
			if self.leftChild == None:
				return False if other.leftChild != None
			else:
				return False if self.leftChild != other.leftChild

			if self.rightChild == None:
				return False if other.rightChild != None
			else:
				return False if self.rightChild != other.rightChild

			return True

		def __hash__(self):
			return hash( (self.parent, self.leftChild, self.rightChild) )





	class UnaryRule():

		def __init__(self, parent, child):
			self.parent = parent
			self.child = child

		def getParent(self):
			return self.parent

		def getChild(self):
			return self.child

		def getScore(self):
			return self.score

		def setScore(self, score):
			self.score = score

		def toString(self):
			return self.parent + "->" + self.child + " %% " + self.score

		def __eq__(self, other):
			return False if not isinstance(other, self.__class__)
			
			if self.parent == None:
				return False if other.parent != None
			else:
				return False if self.parent != other.parent

			if self.child == None:
				return False if other.child != None
			else:
				return False if self.child != other.child

			return True

		def __hash__(self):
			return hash( (parent, child) )



