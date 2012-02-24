
class Node:
    def __init__(self,char):
	if not type(char) == type('') or\
		not len(char) == 1:
	    raise TypeError("Bad Node character %s" % char)
	self.adjacent = []
	if char == 'q':
	   self.char = 'qu'
	else:
	    self.char = char
	self.marked = False
    def __str__(self):
	return self.char

class WordBoard:
    """
    The boggle board and letters.
    """   
    __dir__ = [
	(-1,-1),
	(-1,0),
	(-1,1),
	(0,-1),
	#(0,0), <-- Not adjacent to self
	(0,1),
	(1,-1),
	(1,0),
	(1,1)]
 
    MIN_WORD_LENGTH = 3
    BOARD_SIZE      = 4
    
    def __init__(self,boardInput=None,boardSeed=None):
        self.board = boardInput
	self.matrix = self.__get2dmatrix(self.board)
    
    def __str__(self):
	boardString = ''
	for row in self.board:
	    boardString+=''.join(row)+'\n'
	return boardString

    def __get2dmatrix(self,list2d):
	matrix = []

	for i in xrange(len(list2d)):
	    matrix.append([])
	    for j in xrange(len(list2d[0])):
		node = Node(list2d[i][j])
		matrix[-1].append(node)
		for x,y in self.__dir__:
		    try:
	    		node.adjacent.append(list2d[i+x][j+y])
		    except IndexError:
			pass
	return matrix

    def __getattr__(self,attr):
	if attr == 'words':
	    self.__getWords__(self.MIN_WORD_LENGTH)
	    self.words = set(self.words)
	    return self.words	
	else:
	    raise AttributeError

    def __getWords__(self,min_length):
	self.words = []
	for i in xrange(self.BOARD_SIZE):
	    for j in xrange(self.BOARD_SIZE):
		self.__recurse((i,j),'')

    def early_escape(self,word):
	return False

    def __recurse(self,pos,word):
	x,y = pos
	if x < 0 or x >= self.BOARD_SIZE or y < 0 or y >= self.BOARD_SIZE:
	    return
	node = self.matrix[x][y]
	if node.marked:
	    return

	if self.early_escape(word):
	    return
	
	if self.dict.checkWord(word) and len(word) >= self.MIN_WORD_LENGTH:
	    self.words.append(word)

	node.marked = True
	for i,j in self.__dir__:
	    self.__recurse((x+i,y+j),'%s%s' % (word,node.char))
	node.marked = False
	return
	
