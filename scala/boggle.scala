object Settings {

	def dice = List("iefyeh",
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
	)
	
	def min_word_length = 3

}




class Board(board: List[String]) {

	def size = 4
	
	def brd = board

	override def toString = {
		var str = ""
		brd.foreach({ row => str += row + "\n" })
		str
	}
		
}


object Main {
	def main(args: Array[String]) {
		val board = new Board(List("abcd","bwer","erte","erty"))
		println(board)
	}
}