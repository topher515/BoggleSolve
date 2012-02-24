import random
import sys
from time import clock
from dictionary import SimpleDictionary as Dictionary

dice = [
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
"bqajmo", # q is actually 'qu'
"aaciot",
"camdep",
"aybilt",
"hmosar",
"wirglu"
]

min_word_length = 3

class Board(object):
	
	size = 4
	
	def __init__(self,board):
		if len(board) != len(dice):
			raise ValueError
		self.board = board 
	
	@staticmethod
	def random(seed=None):
		if seed:
			random.seed(seed)
		board = []
		for dice in random.sample(dice,dice.length):
			board.append(random.choice(dice))
		return Board(board)
	
	def __str__(self):
		board = []
		for index,char in enumerate(self.board):
			if index % self.size == 0 and index != 0:
				board.append('\n')
			board.append(char)
		return ''.join(board)
		
	def at(self,x,y):
		if x >= self.size or y >= self.size or x < 0 or y < 0:
			return None
		char = self.board[x+self.size*y]
		return char if char != 'q' else 'qu' # A 'q' is always a 'qu' in boggle
	
		
def solve(board):
	
	d = Dictionary.load()
	
	words = []
	
	def check(x,y,checking,checked):
		if not board.at(x,y) or checked.get((x,y)):
			return
			
		checked[(x,y)] = True
		checking.append(board.at(x,y))
		
		#print '%s (%s,%s)' % (checking,x,y)
		
		if not d.checkPrefix(checking):
			checking.pop()
			del checked[(x,y)]
			return
			
		if len(checking) >= min_word_length and d.checkWord(checking):
			words.append(''.join(checking))
		
		for y_delta in (-1,0,1):
			for x_delta in (-1,0,1):
				check(x+x_delta,y+y_delta,checking,checked)
				
		del checked[(x,y)]
		checking.pop()
		return 

	for x in xrange(board.size):
		for y in xrange(board.size):
			check(x,y,[],{})
	
	return words
	

def main(args):
	if len(args) > 1:
	
		if len(args[1]) == 16:
			print "Using %s as board..." % args[1]
			b = Board(args[1])
		else:
			print "Using random board with seed %s..." % args[1]
			print "(If you want to specify a board it must be 16 chars.)"
			b = Board.random(args[1])
	else:
		print "Using random board..."
		b = Board.random()
	
	print b
	solved = solve(b)
	solved.sort()
	print solved
	
if __name__ == "__main__":
	main(sys.argv)
		
			