require 'set'
require './bsearch.rb'

class Dictionary
  def initialize(words,allow_proper_names=false)
    if allow_proper_names
      @word_list = words.reject {|x| x == ""}
    else
      @word_list = words.reject {|x|
        x[0,1] == x[0,1].capitalize or x == ""
      }
    end
    
    @word_list.collect! {|x| x[0,x.length-1]}
    
    @word_list.sort!
    @word_set = @word_list.to_set
  end
  
  def length
    return @word_list.length
  end
    
  def check_word(word)
    @word_set.member? word
  end
    
  def check_prefix(prefix)
    return @word_list.bsearch_first {|x| x[0, prefix.length] <=> prefix}
  end
  
  def self.from_file(filename)
    dict_lines = IO.readlines(filename)
    return Dictionary.new(dict_lines)
  end
    
  def self.load()
    self.from_file('/usr/share/dict/words')
  end
    
end


def test
  dict = Dictionary.load()
  for word in ["ball","nut","foobar","temple","ham","hamfisted"] do
    resp = (dict.check_word word) ? '' : "not "
    puts "#{word} is a #{resp}word"
  end
  
  for word in ["pre","wampa","su","rem","xpxxx"] do
    resp = (dict.check_prefix word) ? '' : "not "
    puts "#{word} is a #{resp}prefix"
  end
end