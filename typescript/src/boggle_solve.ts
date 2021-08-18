// import { TrieSearch } from '@committed/trie-search';
import { Trie } from "prefix-trie-ts";
import { parse } from 'ts-command-line-args';
import { createReadStream, ReadStream } from 'fs';
import seedrandom from 'seedrandom';

import { sample, range, sortBy } from 'lodash';
import readline from 'readline';

const SIZE = 4
const DEFAULT_DICT = '/usr/share/dict/words'
const IGNORE_PROPER_NAMES = true
const DICE = [
    'iefyeh', 'eptslu', 'henips', 'lecars',
    'avndze', 'dkunto', 'snedwo', 'tgievn',
    'eylugk', 'fbirxo', 'bqajmo', // q is actually 'qu'
    'aaciot', 'camdep', 'aybilt', 'hmosar',
    'wirglu'
]

interface SolveArgs {
    board?: string;
    seed?: string;
    dict?: string;
    help?: boolean;
}

function generateRandomBoard(rng: (()=> number), dice: Array<string>): string {
    return sortBy(dice, rng()).map(sample).join('')
}

async function loadWordsAsTrie(stream: ReadStream) {
    const trie = new Trie()
    const rl = readline.createInterface({
        input: stream,
        crlfDelay: Infinity
    });
    for await (const line of rl) {
        if (IGNORE_PROPER_NAMES && line[0] == line[0].toUpperCase()) {
            continue
        }
        trie.addWord(line)
    }
    return trie
}

function parseBoard(value: string) {
    if (value.length != SIZE * SIZE) {
        throw new Error(`Invalid board ${value}`)
    }
    return value
}

function solve() {

}

async function main() {
    const args = parse<SolveArgs>(
        {
            board: { type: parseBoard, optional: true },
            seed: { type: String, optional: true },
            dict: { type: String, optional: true },
            help: { type: Boolean, optional: true, alias: 'h', description: 'Prints this usage guide' },
        },
        {
            headerContentSections: [{ header: 'Boggle Solve', content: 'Thanks for using Our Awesome Library' }],
        }
    );

    let board = args.board
    if (board) {
        console.log(`Solving for board: "${board}"...`)
    } else {
        const seed = args.seed || range(5).map(()=> sample("abcdefghijklmnopqrstuvwxyz0123456789")).join('')
        board = generateRandomBoard(seedrandom(seed), DICE)
        console.log(`Used random seed "${seed}" to generate board: "${board}". Solving...`)
    }

    const trie = loadWordsAsTrie(createReadStream(args.dict ? args.dict : DEFAULT_DICT))
    const solutions = solve()
        

}

main()