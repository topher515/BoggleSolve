#!/usr/bin/env python

'''Solve boggle boards'''

from typing import TextIO
import sys
import string
import argparse
import random
from random import sample, choice
import pygtrie

MIN_WORD_LENGTH = 3
DICE = (
    'iefyeh', 'eptslu', 'henips', 'lecars',
    'avndze', 'dkunto', 'snedwo', 'tgievn',
    'eylugk', 'fbirxo', 'bqajmo', # q is actually 'qu'
    'aaciot', 'camdep', 'aybilt', 'hmosar',
    'wirglu'
)
SIZE = 4
IGNORE_PROPER_NAMES = True


def solve(board: str, dict_trie: pygtrie.CharTrie, size: int):
    '''board is a 16-digit string; dict_trie is a pygtrie representation of a word dictionary'''

    def board_at(x, y):
        '''Return value at board coord (x, y). `None` if off board.'''
        if x >= size or y >= size or x < 0 or y < 0:
            return None
        char = board[x + size * y]
        if char == 'q':
            return 'qu'
        return char

    words = set()
    checking = []
    checked = {}

    def check(x:int, y:int):
        '''
        Check the board at position (x, y) for all words which can be built
        '''
        if not board_at(x, y) or checked.get((x, y)):
            return None

        checking.append(board_at(x, y))
        possible_word = ''.join(checking)

        if len(possible_word) >= MIN_WORD_LENGTH and dict_trie.has_key(possible_word):
            words.add(possible_word)

        if dict_trie.has_subtrie(possible_word):
            # We must go deeper!
            checked[(x, y)] = True # You cannot use the same die twice in a single boggle word
            for x_d, y_d in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                check(x+x_d, y+y_d)
            del checked[(x, y)]

        checking.pop()

    for i in range(size):
        for j in range(size):
            check(i, j)
    return words


def generate_random_board(dice:tuple):
    '''Generate random board from dice'''
    return ''.join([choice(die) for die in sample(dice, len(dice))])


def load_words_as_trie(dict_file: TextIO):
    '''Load words dictionary file as Trie data type'''
    trie = pygtrie.CharTrie()
    for line in dict_file:
        if IGNORE_PROPER_NAMES and line[0].upper() == line[0]:
            continue
        trie[line.strip()] = True
    return trie


def board_type(value:str):
    '''Enforce a 16 char requirement in board input'''
    str_val = str(value)
    if len(str_val) != 16:
        raise argparse.ArgumentTypeError('Must be 16-character string')
    return str_val


def main(args):
    parser = argparse.ArgumentParser(description='Solve boggle board.')
    parser.add_argument('--board', type=board_type, help='Board specified as 16-char string')
    parser.add_argument('--seed', type=str, help='Random seed with which to init board')
    parser.add_argument('--dict', type=argparse.FileType('r'), help='File path to dictionary', default='/usr/share/dict/words')

    parsed = parser.parse_args(args)

    seed = parsed.seed or ''.join(sample(string.ascii_letters + string.digits, 5))
    random.seed(seed)
    trie = load_words_as_trie(parsed.dict)

    if parsed.board:
        board = parsed.board
        print(f'Solving for board: "{board}"', file=sys.stderr)
    else:
        board = generate_random_board(DICE)
        print(f'Used random seed "{seed}" to generate board: "{board}". Solving...', file=sys.stderr)
    
    solutions = solve(board, trie, SIZE)

    for word in sorted(solutions):
        print(word)

if __name__ == '__main__':
    main(sys.argv[1:])
