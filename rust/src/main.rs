
use clap::{App, Arg};
use rand::{SeedableRng};
use rand_xorshift::XorShiftRng;
use rand::seq::SliceRandom;
use std::fs::{File};

// LEARN: look for a file named `my.rs` or `my/mod.rs` and will
// insert its contents inside a module named `my` under this scope
// Seehttps://doc.rust-lang.org/rust-by-example/mod/split.html
mod prefix_dict;

const SIZE : usize = 4;
const BOARD_LEN : usize = SIZE * SIZE;
// const MIN_WORD_LENGTH : u8 = 3;
const DEFAULT_DICT : &str = "/usr/share/dict/words";

type Die = [char; 6];
const DICE : [Die; BOARD_LEN]= [
    ['i','e','f','y','e','h'], 
    ['e','p','t','s','l','u'],
    ['h','e','n','i','p','s'], 
    ['l','e','c','a','r','s'],
    ['a','v','n','d','z','e'],
    ['d','k','u','n','t','o'],
    ['s','n','e','d','w','o'],
    ['t','g','i','e','v','n'],
    ['e','y','l','u','g','k'],
    ['f','b','i','r','x','o'],
    ['b','q','a','j','m','o'],
    ['a','a','c','i','o','t'],
    ['c','a','m','d','e','p'],
    ['a','y','b','i','l','t'],
    ['h','m','o','s','a','r'],
    ['w','i','r','g','l','u']
];



type Board = [char; 16];



fn generate_random_board(mut rng: XorShiftRng) -> Board {
    // Shuffle dice
    let mut dice : Vec<Die> = DICE.to_vec();
    dice.shuffle(&mut rng);

    // Choose a random side (char) of die
    let mut board : Board = [' '; BOARD_LEN];
    for (i, die) in dice.iter().enumerate() {
        // LEARN: expect a Some or Ok result (lik .unwrap)
        // https://learning-rust.github.io/docs/e4.unwrap_and_expect.html
        let &die_char = die.choose(&mut rng).expect("Found empty dice");
        board[i] = die_char
    }
    board
}


fn main() {
    
    let matches = App::new("Boggle Solve")

        .arg(
            Arg::new("board")
                .about("board to solve")
                .takes_value(true)
                .long("board")
                .required(false)
                .conflicts_with("seed")
        )
        .arg(
            Arg::new("seed")
                .about("random seed to use when generating a board")
                .takes_value(true)
                .long("seed")
                .required(false)
        )
        .arg(
            Arg::new("dict")
                .about("file path of a word dictionary")
                .takes_value(true)
                .long("dict")
                .default_value(DEFAULT_DICT)
                .required(false)
        )
        .get_matches();

    let board =
        if let Some(board_inp) = matches.value_of("board") {
            eprintln!("Solving for board: {}", board_inp);

            let mut board_mut : Board = [' '; 16];
            for (i,c) in board_inp.chars().enumerate() {
                board_mut[i] = c;
            }
            board_mut

        } else {

            let rng : XorShiftRng = 
                match matches.value_of("seed") {
                    Some(seed_inp) => {
                        let seed : u64 = seed_inp.parse::<u64>().expect("Seed must be an integer");
                        SeedableRng::seed_from_u64(seed)
                    }
                    None => SeedableRng::seed_from_u64(0xDEADBEEF)
                };

            let board : Board = generate_random_board(rng);
            eprintln!("Generated random board {:?} from seed", board);
            board
        };

    let dict_path = matches.value_of("dict").expect("Missing dict path");
    let words_file = File::open(dict_path).expect(&format!("Could not open file '{}'", dict_path)[..]);
    let prefdict = prefix_dict::PrefixDict::new(words_file);

    
    // solutions = solve(board, trie, SIZE)

    // for word in sorted(solutions):
    //     print(word)


}
