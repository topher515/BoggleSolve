from __future__ import with_statement
import os

class Dictionary(object):
	def checkWord(self,word):
		pass
	def checkPrefix(self,prefix):
		pass

class SimpleDictionary(Dictionary):
    def __init__(self,filename="dictionary.txt"):
        self.dictionary = set()
        self.size = 0
        dictionary = []

		filename = os.path.join(os.path.dirname(__file__),filename)
        
        with open(filename,'r') as dictFile:
	        for line in dictFile:
   	            dictionary.append(line[0:-1])
   	            self.size += 1
        self.dictionary = set(dictionary)
        self.dictionaryList = dictionary
        
    def checkWord(self,word):
        return word in self.dictionary
        
    def checkPrefix(self,prefix):
        #import re
        #regex = re.compile(prefix + "[a-z]+")
        #for word in self.dictionary:
        #    regex.match(self.dictionary)
        self.cnt = 0
        return self.__checkPrefix(prefix,0,(self.size-1))
    
    def __checkPrefix(self,prefix,least,most):
        self.cnt +=1
        if self.cnt > 100: 
            return None
        
        checkAt = least+(most-least)/2
        #print checkAt
        
        if (checkAt <= 0):
            return False
        
        checkWord = self.dictionaryList[checkAt] 
        #print "checking %s" % (checkWord)
        checkLen = min(len(prefix),len(checkWord))
            
                    
        for i in range(0,checkLen):  
            #print "checking %s and %s" % (prefix[i], checkWord[i])
            if prefix[i] < checkWord[i]:
                #print "lessthan\n"
                return self.__checkPrefix(prefix,least,checkAt-1)
            elif prefix[i] > checkWord[i]:
                #print "greaterthan\n"
                return self.__checkPrefix(prefix,checkAt+1,most)
            else:
                if i+1 == len(prefix):
                    return checkWord
                
        return self.__checkPrefix(prefix,checkAt+1,most)
        
        
    def info(self):
        return "The dictionary contains %d entries" % self.size
    
    def prefixTester(self):
        cnt = 0
        step = round(self.size/100)
        #print step
        for word in self.dictionaryList:
            cnt+=1
            if not self.checkPrefix(word):
                print "Couldn't find prefix %s" % word
    
    def dump(self):
        print self.dictionary

class TrieDictionary(Dictionary):

	def checkWord(self,word):
		if not word: return False
		return self.__check_word(word,self.root)

	def __check_word(self,left_to_check,node):
		if not left_to_check:
			if node.get('\n') == {}: return True
			else: return False
		if left_to_check[0] in node:
			return self.__check_word(left_to_check[1:],node[left_to_check[0]])
		else:
			return False

	def checkPrefix(self,prefix):
		return self.__check_prefix(prefix,self.root)

	def __check_prefix(self,left_to_check,node):
		if not left_to_check:
			return True
		if left_to_check[0] in node:
			return self.__check_prefix(left_to_check[1:],node[left_to_check[0]])
		else:
			return False

	def __add_chars(self,left_to_check, node):
		""" Continue along the tree until we get to the end then add with the
		__add_chars_eow method """
		if len(left_to_check) == 0:
			return # This might happen if we tried to add a word already in the dictionary
		if left_to_check[0] in node:
			self.__add_chars(left_to_check[1:],node[left_to_check[0]])
		else:
			self.__add_chars_eow(left_to_check,node)

	def __add_chars_eow(self,left_to_add,node):
		""" If we know that a word isn't in our dict, then we can use this method
		to just keep adding chars """
		if left_to_add:
			node[left_to_add[0]] = {}
			self.__add_chars_eow(left_to_add[1:],node[left_to_add[0]])

	def __init__(self,filename="dictionary.txt"):
		self.root = {}
		with open(filename,'r') as dictFile:
			for word in dictFile:
				self.__add_chars(word,self.root)
