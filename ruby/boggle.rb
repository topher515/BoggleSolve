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



class Board

  @@size = 4
  
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
      if index % @@size == 0 and index != 0
        board.push "\n"
      end
      board.push @board[index]
    end
    board.join ''
  end
  
  def at(x,y)
    if x >= @@size or y >= @@size or x < 0 or y < 0
      return nil
    end
    char = @board[x + @@size*y]
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
    
    if checking.length >= Boggle.const_get(:MIN_WORD_LENGTH) and d.check_word(checking.join '')
      words.push(checking.join '')
    end
    
    for y_delta in [-1,0,1] do
      for x_delta in [-1,0,1]
        check(d,board,words,x+x_delta,y+y_delta,checking,checked)
      end
    end  
    checked.delete([x,y])
    checking.pop()
  end
  
  for x in (0...Board.size)
    for y in (0...Board.size)
      check(d,board,words,x,y,[],{})
    end
  end
    
  return words
end
  

def main(args)
  if args.length > 1
    if args[1].length == 16
      puts "Using #{args[1]} as board..."
      b = Board.new(args[1])
    else
      puts "Using random board with seed #{args[1]}" +
          "(If you want to specify a board it must be 16 chars.)"
      b = Board.random(args[1])
    end
    
  else
    puts "Using random board..."
    b = Board.random()
  end
  
  puts b
  solved = solve(b)
  solved = solved.to_set().to_a().sort()
  puts solved
end
  
main(ARGV)