require('./dictionary.js')

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
"bqajmo", // q is actually 'qu'
"aaciot",
"camdep",
"aybilt",
"hmosar",
"wirglu"
]

min_word_length = 3

function Board(board_init) {
	if (board_init.length != dice.length)
		throw 'BoardSizeError'
	
	// Private vars //
	var board = board_init;
	
	this.__defineGetter__('size',function() {
		return Board.size
	})
	
	// Return the string representation of this board
	this.toString = function() {
		board_list = []
		for (i in board) {
			if (i % Board.size == 0 && i != 0)
				board_list.push('\n')
			board_list.push(board[i])
		}
		return board_list.join('')
	}
	
	// Return the char at this board location
	this.at = function(x,y) {
		if (x >= Board.size || y >= Board.size || x < 0 || y < 0)
			return null
		letter = board[x+Board.size*y]
		return letter == 'q' ? 'qu' : letter // A 'q' is always a 'qu' in boggle
	}
}

// Static public variables/methods
Board.size = 4;
Board.random = function(seed) {
	// TODO Implement a seedable random number generator
	
	board = []
	for (var i in dice) {
		dice = dice[i];
		board.push(dice[Math.floor(Math.random()*dice.length)]);
	}
	return new Board(board)
}


function solve(board) {
	
	var d = Dictionary.load()
	
	var words = []
	
	var check = function(x,y,checking,checked) {
		if (!Boolean(board.at(x,y)) || checked[x+','+y])
			return
		
		checked[x+','+y] = true
		checking.push(board.at(x,y))
		
		if (!d.checkPrefix(checking)) {
			checking.pop()
			delete checked[x+','+y]
			return
		}
		
		if (checking.length >= min_word_length && d.checkWord(checking))
			words.push(checking.join(''))
		
			
		add = [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
		for (i in add) {
			check(x+add[i][0],y+add[i][1],checking,checked)
		}
			
		delete checked[x+','+y]
		checking.pop()
		return
	}
	
	for (x=0; x<Board.size; x++) {
		for (y=0; y<Board.size; y++) {
			check(x,y,[],{})
		}
	}
	
	return words
}

function main(args) {
	if (args.length > 0) {
		if (args[0].length == 16) {
			console.log("Using " + args[0] + " as board...")
			b = new Board(args[0])
		} else {
			console.log("Using random board with seed " + args[0] + "...")
			console.log("(If you want to specify a board it must be 16 chars.)")
			b = Board.random(args[0])
		}
	} else {
		console.log("Using random board...")
		b = Board.random()
	}
	
	console.log(b)
	solved = solve(b)
	solved.sort()
	console.log(solved)
}

main(arguments)