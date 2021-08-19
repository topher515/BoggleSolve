
use clap::{App, Arg};
// use rand::rngs::{StdRng};
use rand::{SeedableRng, Rng};
use rand_xorshift::XorShiftRng;

// /// Boggle Solve
// #[derive(Clap)]
// #[clap(version = "0.1.0", author = "Chris Wilcox <ckwilcox@gmail.com>")]
// #[clap(setting = AppSettings::ColoredHelp)]
// struct Opts {

//     board: String,
//     seed: String,
//     #[clap(short, long, default_value = "'/usr/share/dict/words'")]
//     dict: String,
// }

// #[derive(Debug)]
type Board = [char; 16];


fn generate_random_board() -> Board {
    [
        'a','b','c','d',
        'e','f','g','h',
        'i','j','k','l',
        'm','n','o','p'
    ]
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

        } else if let Some(seed_inp) = matches.value_of("seed") {
            let seed : u64 = seed_inp.parse::<u64>().unwrap();
            let rng : XorShiftRng = SeedableRng::seed_from_u64(seed);
            // random.seed()
            // let board = generate_random_board(DICE)
            generate_random_board()

        } else {
           panic!("foo")
        };

    // solutions = solve(board, trie, SIZE)

    // for word in sorted(solutions):
    //     print(word)


}
