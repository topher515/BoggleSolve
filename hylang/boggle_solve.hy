(import sys string argparse random pygtrie)
(import [random [sample choice]]
        [typing [TextIO]])

(setv MIN_WORD_LENGTH 3
      SEED_LEN 5
      SIZE 4
      IGNORE_PROPER_NAMES True)
; # q is actually "qu" 
(setv DICE [
    "iefyeh" "eptslu" "henips" "lecars" 
    "avndze" "dkunto" "snedwo" "tgievn" 
    "eylugk" "fbirxo" "bqajmo" 
    "aaciot" "camdep" "aybilt" "hmosar" 
    "wirglu"
    ])

    
(defn solve [^str board  ^pygtrie.CharTrie dict-trie  ^int size] 
    (defn board-at [^int x  ^int y]
        (if (or (>= x size) (>= y size) (< x 0) (< y 0)) 
            None
            (do
                (setv char (get board (+ x (* size y))))
                (if (= char "q") "qu" char))))
    
    (setv words #{}
          checking []
          checked {})

    (defn check [^int x  ^int y]
        (if (or (not (board-at x y)) (.get checked (, x y)) ) (return None))

        (.append checking (board-at x y))

        (setv possible-word ((. "" join) checking))
        (if (and (> (len possible-word) MIN_WORD_LENGTH) (dict-trie.has_key possible-word))
            ; Found a word!
            (.add words possible-word))

        (if (dict-trie.has_subtrie possible_word)
            ; We must go deeper!
            (do
                (assoc checked (, x y) True)
                (for [[x_d y_d] [(, -1 -1) (, -1 0) (, -1 1) (, 0 -1) (, 0 1) (, 1 -1) (, 1 0) (, 1 1)]]
                    (check (+ x x_d) (+ y y_d)))
                (del (get checked (, x y)))
            ))
        
        (.pop checking)
        
    )

    (for [i (range size)] 
        (for [j (range size)]
            (check i j)))
    words 
)


(defn generate-random-board [dice]
    "Generate random board from dice"
    ((. "" join)
        (lfor die (sample dice (len dice)) (choice die))))


(defn load-words-as-trie [^TextIO fp] 
    "Load words file as Trie data type"
    (setv trie (pygtrie.CharTrie))
    (for [line fp]
        (if (and IGNORE_PROPER_NAMES (= (get line 0) (.upper (get line 0))))
            ; skip "proper names", i.e., words that start uppercase
            (continue)
        )
        (assoc trie (.strip line) True))
    trie)

(defn board-type [^str value]
    (if (!= (len value) (* SIZE SIZE)) 
        (raise (argparse.ArgumentTypeError "Must be 16-character string")))
    value)

(defn main [args]
    (setv parser (argparse.ArgumentParser :description "solve boggle board"))
    (parser.add_argument "--board" :type board-type :help f"Board specified as {(* SIZE SIZE)}-char string")
    (parser.add_argument "--seed" :type str :help "Random seed with which to init board")
    (parser.add_argument "--dict" :type (argparse.FileType "r") :help "File path to dictionary" :default "/usr/share/dict/words")
    
    (setv parsed (parser.parse_args args))

    (setv seed (or parsed.seed (sample (+ string.ascii_letters string.digits) SEED_LEN)))
    (setv seed ((. "" join) seed))
    (random.seed seed)

    (if parsed.board 
        (do (setv board parsed.board) 
            (print f"Solving for board: '{board}'" :file sys.stderr))
        (do (setv board (generate-random-board DICE))
            (print f"Used random seed '{seed}' to generate board: {board}. Solving..." :file sys.stderr)
            ))

    (setv trie (load-words-as-trie parsed.dict))
    (setv solutions (solve board trie SIZE))

    (for [word (sorted solutions)] (print word))
)
    

(if (= __name__ "__main__")
    (main (cut (. sys argv) 1)))
