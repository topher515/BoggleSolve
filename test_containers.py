#!/usr/bin/env python3
import sys
import unittest
from subprocess import run

from run_container import image_name, run_bogglesolve_container, DEFAULT_DICT_PATH

EXPECTED_SOLUTIONS = b'aal\naalii\nail\naile\naisle\nalcine\nale\nalen\nalias\nalien\nalin\naln\nani\nanis\naquiline\ncilia\ncine\ncinel\nclag\nclan\nclang\ncline\nclinia\nelain\nels\nelsin\nens\ngain\ngaine\ngains\ngal\ngale\ngalenic\ngali\ngan\ngas\nilia\niliau\ning\ninial\ninquiline\nisle\nlag\nlai\nlain\nlaine\nlan\nlas\nlei\nlenis\nlens\nliang\nlie\nlien\nliin\nlin\nline\nlinie\nlis\nnaa\nnag\nnail\nnain\nnais\nnasi\nnei\nngai\nnil\nquag\nquail\nquale\nquan\nquasi\nquila\nquin\nquinia\nquinic\nquis\nquisle\nsaa\nsag\nsai\nsail\nsain\nsal\nsale\nsalic\nsaline\nsan\nsang\nsial\nsialic\nsil\nsile\nsilen\nsileni\nsilenic\nsiliqua\nsin\nsina\nsinal\nsine\nsing\nsla\nslag\nslain\nslang\nsline\nsnag\nsnail\nsnails\nsquail\nsquin\nsuine\nusnic\n'
TEST_BOARD = 'sgnscqaiiliaensu'


def build_bogglesolve_image(dir_name: str):
    run(["docker", "build", "--rm", "-t", image_name(dir_name), "."], check=True, cwd=f"./{dir_name}")


class TestViaDocker(unittest.TestCase):

    dict_words_path = DEFAULT_DICT_PATH

    def test_python2(self):
        build_bogglesolve_image('python2')
        proc = run_bogglesolve_container('python2', [TEST_BOARD], dict_path=self.dict_words_path)
        self.assertEqual(proc.stdout, EXPECTED_SOLUTIONS)

    def test_python3(self):
        build_bogglesolve_image('python3')
        proc = run_bogglesolve_container('python3', ["--board", TEST_BOARD], dict_path=self.dict_words_path)
        self.assertEqual(proc.stdout, EXPECTED_SOLUTIONS)

    def test_hylang(self):
        build_bogglesolve_image('hylang')
        proc = run_bogglesolve_container('hylang', ["--board", TEST_BOARD], dict_path=self.dict_words_path)
        self.assertEqual(proc.stdout, EXPECTED_SOLUTIONS)



if __name__ == '__main__':
    if len(sys.argv) > 1:
        TestViaDocker.dict_words_path = sys.argv.pop()
    unittest.main(verbosity=2)