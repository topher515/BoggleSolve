from __future__ import with_statement
import os
from bisect import bisect_left as bisect
import string

class Dictionary(object):
	def checkWord(self,word):
		pass
	def checkPrefix(self,prefix):
		pass

class SimpleDictionary(object):
	def __init__(self,words,allow_proper_names=False):

		if allow_proper_names:
			self.dictionaryList = words
		else:	
			self.dictionaryList = [x for x in words if x[0].upper() != x[0]]

		self.dictionaryList.sort()
		self.dictionarySet = set(self.dictionaryList)
	
	def __len__(self):
		return len(self.dictionarySet)

	def checkWord(self,word):
		return ''.join(word) in self.dictionarySet
	
	def checkPrefix(self,prefix):
		""" Return None if the prefix is not found in the dictionary
		otherwise return the first word matched (there may be other words
		which match this prefix)."""
		#self.cnt = 0
		#return self.__checkPrefix(prefix,0,(self.size-1))
		ins_point = bisect(self.dictionaryList,''.join(prefix))
		try:
			if self.dictionaryList[ins_point].startswith(''.join(prefix)):
				return self.dictionaryList[ins_point]
			else:
				return None	 
		except IndexError:
			return None
	  
	def dump(self):
		print self.dictionaryList

	@staticmethod
	def fromFile(filename):
		lines = []
		with open(filename,'r') as dictFile:
			for line in dictFile:
				lines.append(line[0:-1])
		return SimpleDictionary(lines)

	@staticmethod
	def load():
		return SimpleDictionary.fromFile("/usr/share/dict/words")
