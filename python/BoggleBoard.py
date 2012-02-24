from WordBoard import WordBoard

die = [
"iefyeh",
"eptslu",
"henips",
"lecars",
"avndze",
"dkunto",
"snedwo",
"tgievn",
"eylugk",
"fbirxo",
"bqajmo",   # q is really qu
"aaciot",
"camdep",
"aybilt",
"hmosar",
"wirglu"
]


class BoggleBoard(WordBoard):

    def __init__(self,boardInput=None,boardSeed=None):

	#from Dictionary import TrieDictionary as Dictionary
	from Dictionary import SimpleDictionary
	self.dict = Dictionary()

	if boardInput:
	    board = boardInput
	else:
	    if not boardSeed:
		from time import clock
	    	boardSeed = clock()
	    board = self.__get2dList__(boardSeed)
	WordBoard.__init__(self,board,None)

    def early_escape(self,word):
	if len(word) <= 2:
	    return False
	maybe_word = self.dict.checkPrefix(word)
    	if maybe_word == None:
	    return True
	else:
	    return False

    def __get2dList__(self,seed):
        import random
        import string
        b = []
        alphabet = string.ascii_lowercase
        random.seed(seed)

	# copy die
	die_copy = []
	for dice in die:
		die_copy.append(str(dice))

        for i in xrange(self.BOARD_SIZE):
	    b.append([])
	    for j in xrange(self.BOARD_SIZE):
		chosen_die = random.choice(die_copy)
		chosen_char = random.choice(chosen_die)
		b[-1].append( chosen_char )
        return b

