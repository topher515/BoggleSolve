#!/usr/bin/env python

import sys
import os

def usage(msg):
    print '%s: -dchb' % sys.argv[0]
    print '   %s' % msg
    print '   Try %s -h for help' % sys.argv[0]


def main(args=None):
    if args == None:
	args = sys.argv[1:]

    if len(args) < 1:
	usage('No arguments given.')
	return 1

    board = words = code = file = None

    from getopt import getopt
    (opts,args) = getopt(args,'d:c:hsb:f:')
    for opt,val in opts:
	if '-h' == opt:
	    print """options:
	-d dictionary_file	The dictionary file to use. (Default dictionary.txt)
	-h			Display this help text.
	-b board_string		Specify the Boggle board with a string. String must be 16 alphabetical characters
				long and signifies the boggle letters read left to right starting at the upper left.
	-c code			Some alphanumeric code used to generate the board. Reusable randomness!
"""
	    return 0

	if '-d' == opt:
	    if not os.path.isfile(opt):
		print "Not a valid dictionary"
		return 1
	    	

	if '-c' == opt:
	    code = val

	if '-b' == opt:
	    board = val

	if '-f' == opt:
	    file = val

    readyBoard = []
    if board:
	if not len(board) == 16:
	    print "Boggle board must be 16 alpha characters long."
	    return 1
	cnt = 0 
   	for each in board:
	    if cnt % 4 ==0:
	    	readyBoard.append([])
	    readyBoard[-1].append(each)
	    cnt+=1

    elif file:
	if os.path.isfile(file): 
	    f = open(file,'r')
	    readyBoard = f.read()
	
	
    import BoggleBoard
    
    if code and not readyBoard:
	usrmsg("Generating Boggle Board to solve!")
	b = BoggleBoard.BoggleBoard(boardSeed=code)
	usrmsg("The board:\n")
	usrmsg(b)
    	words = b.words
    elif readyBoard:
	#usrmsg("Got Board input:\n%s" % readyBoard)
	usrmsg("The board:\n")
	b = BoggleBoard.BoggleBoard(boardInput=readyBoard)
  	usrmsg(b)
	words = b.words
    words = list(words)
    words.sort()

    def lensrt(x,y):
	if len(x) < len(y):
	    return -1
	elif len(x) > len(y):
	    return 1
	else:
	    return 0

    words.sort(lensrt)
    for w in words:
	usrmsg(w)

def usrmsg(msg):
    print msg

if __name__ == '__main__':
    sys.exit(main())

