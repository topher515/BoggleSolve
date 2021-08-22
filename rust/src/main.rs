// LEARN:
// TODO: Learn this probably: https://rust-unofficial.github.io/too-many-lists/

use std::process::exit;
use clap::{App, Arg};
use rand::{SeedableRng};
use rand_xorshift::XorShiftRng;
use rand::seq::SliceRandom;
use std::fs::{File};
use std::collections::HashSet;

// LEARN: look for a file named `my.rs` or `my/mod.rs` and will
// insert its contents inside a module named `my` under this scope
// Seehttps://doc.rust-lang.org/rust-by-example/mod/split.html
mod prefix_dict;
use prefix_dict::PrefixDict as PrefixDict;

const SIZE : usize = 4;
// const SIZE_USIZE : usize = 4;
const BOARD_LEN : usize = SIZE * SIZE;
const MIN_WORD_LENGTH : usize = 3;
const DEFAULT_DICT : &str = "/usr/share/dict/words";

type Board = [char; BOARD_LEN];
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

const DIRS : [[i32; 2]; 8] = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]];

// LEARN: To use this in as hashset these methods must be implemented,
// but the compiler can do it for us
// see: https://stackoverflow.com/a/31835987/273637
//      https://stackoverflow.com/a/31846475/273637
#[derive(PartialEq, Eq, Hash, Clone, Copy, Debug)]
struct Coord {
    x: i32,
    y: i32
}


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



#[derive(Debug)]
struct SearchState {
    partial_word_vec: Vec<String>,
    prev_coords: HashSet<Coord>,
    at_coord: Coord,
    dir_index: usize,
}


fn solve_from_one_die(board: Board, prefdict: &PrefixDict, &start_coord: &Coord) -> HashSet<String> {

    let mut words : HashSet<String> = HashSet::new();

    let board_at = |coord:Coord| -> Option<String> {
        if coord.x >= (SIZE as i32) || coord.y >= (SIZE as i32) || coord.x < 0 || coord.y < 0 {
            Option::None
        } else {
            let char_at : char = board[(coord.x as usize) + SIZE * (coord.y as usize)];
            match char_at {
                'q' => Some(String::from("qu")),
                _ => Some(char_at.to_string())
            }
        }
    };

    let mut n = 0;

    // Return a new search state item, by finding the next die to examine
    let next = |mut curr_search_state: SearchState| -> (SearchState, Option<SearchState>) {

        let mut at_coord : Coord;
        let char_string : String;
        // Find next valid
        loop {
            if curr_search_state.dir_index == DIRS.len() {
                // This search state has gone through all possible directions
                return (curr_search_state, None)
            }

            let [x_d, y_d] = DIRS[curr_search_state.dir_index];
            at_coord = Coord { x: curr_search_state.at_coord.x + x_d, y: curr_search_state.at_coord.y + y_d };
            if curr_search_state.prev_coords.contains(&at_coord) {
                // We already examined this die while building this word
                curr_search_state.dir_index += 1
            
            } else {
                match board_at(at_coord) {
                    None => { curr_search_state.dir_index += 1; },
                    Some(strn) => {
                        char_string = strn;
                        break;
                    }
                };
            }
        };

        let mut partial_word_vec = curr_search_state.partial_word_vec.clone();
        partial_word_vec.push(char_string);
        let mut prev_coords = curr_search_state.prev_coords.clone();
        prev_coords.insert(curr_search_state.at_coord.clone());
        (
            curr_search_state,
            Some(SearchState {
                partial_word_vec: partial_word_vec, 
                at_coord: at_coord,
                prev_coords: prev_coords,
                dir_index: 0 
            })
        )
    };

    let mut search_state_stack:  Vec<SearchState> = vec![];

    let at_coord = Coord { x: start_coord.x, y: start_coord.y };
    let partial_word_vec = vec![board_at(at_coord).unwrap()];
    let dir_index = 0; // set so the next cycle is [1,0] 
    let prev_coords = HashSet::new();
    search_state_stack.push(
        SearchState { 
            partial_word_vec, 
            at_coord,
            prev_coords,
            dir_index 
        }
    );


    while search_state_stack.len() > 0 {

        // let possible_word : String;
        {
            // LEARN: We have to pop (and later re-push) the search state object because 
            // this block needs to *own* the reference to the search state
            let last_search_state = search_state_stack.pop().unwrap();

            n+=1;
            if n > 1035 {
                exit(1);
            }
            let possible_word = last_search_state.partial_word_vec.join("");

            // LEARN: Note .len() only valid for ascii chars, since it returns byte count
            if possible_word.len() >= MIN_WORD_LENGTH && prefdict.contains(&possible_word) {
                words.insert(possible_word.clone());
            }
            if prefdict.contains_prefix(&possible_word) {

                match next(last_search_state) {
                    (_last_search_state, None)=> {
                        
                        match search_state_stack.pop() {
                            Some(mut prev_search_state) => {
                                prev_search_state.dir_index += 1;
                                search_state_stack.push(prev_search_state);
                            },
                            None => {
                                // Nothing to pop, done with this die
                            }
                        }
                    }
                    (last_search_state, Some(next_search_state))=> {
                        search_state_stack.push(last_search_state);
                        search_state_stack.push(next_search_state);
                    }
                };

            } else {

                match search_state_stack.pop() {
                    Some(mut prev_search_state) => {
                        prev_search_state.dir_index += 1;
                        search_state_stack.push(prev_search_state);
                    },
                    None => {
                        // Nothing to pop, done with this die
                    }
                }
            }
        }
    }
    words
}


fn solve(board: Board, prefdict: &PrefixDict) -> Vec<String> {
    
    let mut words : HashSet<String> = HashSet::new();

    for i in 0..SIZE {
        for j in 0..SIZE {
            let solved = solve_from_one_die(board, prefdict, &Coord { x: i as i32, y: j as i32 });
            for word in solved {
                words.insert(word);
            }
            
        }
    }

    words.into_iter().collect()
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
    let prefdict = PrefixDict::new(words_file);

    let mut solutions = solve(board, &prefdict);
    solutions.sort_unstable();

    for word in solutions {
        println!("{}", word);
    };
}