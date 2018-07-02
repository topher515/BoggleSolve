import unittest
from io import StringIO
from boggle_solve import solve, load_dict_as_trie

class TestStringMethods(unittest.TestCase):

    def test_solve(self):
        board = 'xlrddezhetmobhwj'
        words = ( # Should be present in board
            'bed',
            'bee',
            'beer',
            'beet',
            'eel',
            'home',
            'homer',
            'how',
            'meet',
            'ohm',
            'teer',
            'theb',
            'thee',
            'two',
            'whee',
            'wheel'
        )

        dict_file = StringIO('\n'.join(words + ('extras', 'foobar', 'benedict')))

        trie = load_dict_as_trie(dict_file)

        self.assertEqual(set(words), solve(board, trie, size=4))


if __name__ == '__main__':
    unittest.main()