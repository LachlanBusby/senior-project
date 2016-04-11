import collections
import sys

def accepts(*types, **kw):
	'''Function decorator. Checks decorated function's arguments are
	of the expected types.

	Parameters:
	types -- The expected types of the inputs to the decorated function.
			 Must specify type for each parameter.
	kw    -- Optional specification of 'debug' level (this is the only valid
			 keyword argument, no other should be given).
			 debug = ( 0 | 1 | 2 )

	'''
	if not kw:
		# default level: MEDIUM
		debug = 1
	else:
		debug = kw['debug']
	try:
		def decorator(f):
			def newf(*args):
				if debug is 0:
					return f(*args)
				assert len(args) == len(types)
				for i in range(len(args)):
					if not isinstance(args[i], types[i]):
						msg = info(f.__name__, types, [type(arg) for arg in args], 0)
						if debug is 1:
							print >> sys.stderr, 'TypeWarning: ', msg
						elif debug is 2:
							raise TypeError, msg
				return f(*args)
			newf.__name__ = f.__name__
			return newf
		return decorator
	except KeyError, key:
		raise KeyError, key + "is not a valid keyword argument"
	except TypeError, msg:
		raise TypeError, msg

def info(fname, expected, actual, flag):
	'''Convenience function returns nicely formatted error/warning msg.'''
	format = lambda types: ', '.join([str(t).split("'")[1] for t in types])
	expected, actual = format(expected), format(actual)
	msg = "'{}' method ".format( fname )\
		  + ("accepts", "returns")[flag] + " ({}), but ".format(expected)\
		  + ("was given", "result is")[flag] + " ({})".format(actual)
	return msg

class SequenceMixin(collections.MutableSequence):
	"""A container for manipulating lists of known base class"""
	def __init__(self, concreteType, initList):
		"""Initialize the class"""
		self._type = concreteType

		if not isinstance(initList, list):
			raise TypeError("%s container: constructor called with non-list initializer")

		for elem in initList:
			self._check_type(elem)

		self._list = initList

	def _check_type(self, val):
		if not isinstance(val, self._type):
			raise TypeError("%s container: Cannot store an object of type %s in a sequence of type %s" %(type(self), type(val), self._type))

	def __len__(self):
		"""List length"""
		return len(self._list)

	def __getitem__(self, ii):
		"""Get a list item"""
		return self._list[ii]

	def __delitem__(self, ii):
		"""Delete an item"""
		del self._list[ii]

	def __setitem__(self, ii, val):
		self._check_type(val)
		return self._list[ii]

	def __str__(self):
		return str(self._list)

	def insert(self, ii, val):
		self._check_type(val)
		self._list.insert(ii, val)

	def append(self, val):
		self.insert(len(self._list), val)
