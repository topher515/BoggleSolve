use radix_trie::{Trie};
// use radix_trie::{Trie, TrieCommon};
use std::fs::{File};
use std::io::{BufRead, BufReader};


#[derive(Debug)]
pub struct PrefixDict {
    trie: Trie<String, bool>
}

// pub trait ContainsPrefix {
//     fn contains_prefix(&self, prefix: &str) -> bool;
// }

impl PrefixDict {
    #[inline]
    pub fn new(file: File) -> Self {
        let mut trie: Trie<String, bool> = Trie::new();
        let reader = BufReader::new(file);
        for line in reader.lines() {
            let line = line.expect("Unable to read line");
            trie.insert(line, true);
        }
        PrefixDict { trie }
    }

    #[inline]
    pub fn contains_prefix(&self, prefix: &String) -> bool {
        match self.trie.subtrie(prefix) {
            Some(_value) => true,
            None => false
        }
    }

    #[inline]
    pub fn contains(&self, prefix: &String) -> bool {
        match self.trie.get(prefix) {
            Some(_value) => true,
            None => false
        }
    }
}



// impl ContainsPrefix for PrefixDict {
//     #[inline]
//     fn contains_prefix(&self, prefix: &str) -> bool {
//         match self.trie.subtrie("wil") {
//             Some(value) => true,
//             None => false
//         }
//     }
// }
