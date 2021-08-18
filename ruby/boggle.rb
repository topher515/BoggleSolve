#!/usr/bin/ruby

require './dictionary.rb'

module Boggle
  VERSION = '0.1'
  DICE = [
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
  MIN_WORD_LENGTH = 3
end

SIZE = 4


class Board

  
  def initialize(board)
    if board.length != Boggle.const_get(:DICE).length
      raise ValueError
    end
    @board = board
  end
  
  def self.random(seed=nil)
    if seed
      srand(seed)
    end
    board = []
    for die in Boggle.const_get("DICE") do
      board.insert -1, die[rand(die.length)]
    end
    return Board.new(board)
  end
  
  def to_s
    board = []
    for index in (0...@board.length) do
      if index % SIZE == 0 and index != 0
        board.push "\n"
      end
      board.push @board[index]
    end
    board.join ''
  end
  
  def at(x,y)
    if x >= SIZE or y >= SIZE or x < 0 or y < 0
      return nil
    end
    char = @board[x + SIZE*y]
    char == 'q' ? 'qu' : char
  end
  
end


def solve(board)
  
  d = Dictionary.load()
  
  words = []
  
  def check(d,board,words,x,y,checking,checked)
    if not board.at(x,y) or checked[[x,y]]
      return
    end
    checked[[x,y]] = true
    checking.push(board.at(x,y))
    
    if not d.check_prefix(checking.join '')
      checking.pop()
      checked.delete([x,y])
      return
    end
    
    possible_word = checking.join ''
    if possible_word.length >= Boggle.const_get(:MIN_WORD_LENGTH) and d.check_word(possible_word)
      words.push(possible_word)
    end
    
    for y_delta in [-1,0,1] do
      for x_delta in [-1,0,1]
        check(d,board,words,x+x_delta,y+y_delta,checking,checked)
      end
    end  
    checked.delete([x,y])
    checking.pop()
  end
  
  for x in (0...SIZE)
    for y in (0...SIZE)
      check(d,board,words,x,y,[],{})
    end
  end
    
  return words
end
  

def main(args)
  if args.length > 0
    if args[0].length == 16
      STDERR.puts "Using #{args[0]} as board...\n"
      b = Board.new(args[0])
    else
      STDERR.puts "Using random board with seed '#{args[0]}'" +
          " (If you want to specify a board it must be 16 chars.)"
      b = Board.random(args[0])
    end
    
  else
    STDERR.puts "Using random board..."
    b = Board.random()
  end
  
  solved = solve(b)
  solved = solved.to_set().to_a().sort()
  puts solved
end
  
main(ARGV)