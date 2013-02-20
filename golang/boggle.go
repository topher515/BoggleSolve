// You can edit this code!
// Click here and start typing.
package main

import (
	"fmt"
	"math/rand"
	"time"
	"sort"
	"strings"
	"errors"
	//"io/ioutil"
	"bufio"
	"os"
)

const (
	BOARD_SIZE = 4
	BOARD_LEN = BOARD_SIZE * BOARD_SIZE
	DICT_PATH = "/usr/share/dict/words"
	WORD_MIN_LEN = 3
)


var dice = []string{
"iefyeh",
"eptslu",
"henips",
"lecars",
"avndze",
"dkunto",
"snedwo",
"tgievn",
"eylugk",
"fbirxo",
"bqajmo", // q is actually 'qu'
"aaciot",
"camdep",
"aybilt",
"hmosar",
"wirglu",
}


func LoadFakeDictionary() ([]string) {
	var dict = []string{
		"aardvaark",
		"abacus",
		"pale",
		"test",
		"toast",
		"zylsd",
		"whisk",
	}
	sort.Strings(dict)
	// TODO: Sort dictionary
	return dict
}

func LoadDictionary() ([]string, error) {
	var words = []string{}
	var fp, err = os.Open(DICT_PATH)
	if err != nil {
		panic(err)
	}
	var reader = bufio.NewReader(fp)

	var word = "";
	for ; err == nil; word, err = reader.ReadString('\n') {
		if len(word) < WORD_MIN_LEN {
			continue
		}
		words = append(words, word)
	}
	sort.Strings(words)

	return words, nil
}


func GetPrefixWord(dict []string, prefix string) (string, error) {
	var index = sort.Search(len(dict), func(i int) bool {
			fmt.Println(i, dict[i])
			if dict[i][0:1] > prefix[0:1]{
				return true
			} else if strings.HasPrefix(dict[i], prefix) {
				return true
			}
			return false
		})
	fmt.Println(index)
	if index < len(dict) {
		return dict[index], nil
	}
	return "", errors.New("No prefix found")
}


func Random() ([BOARD_LEN]string) {

	// Roll the dice
	for i := range dice {
	    j := rand.Intn(i + 1)
	    dice[i], dice[j] = dice[j], dice[i]
	}

	// Build a new board
	var board = [BOARD_LEN]string{}
	for i, die := range dice {
		var x = rand.Intn(6)
		board[i] = die[x:x+1]
	}
	return board
}

func Predefined() ([BOARD_LEN]string) {
	return [BOARD_LEN]string{
		"s","e","w","y",
		"p","l","e","x",
		"a","t","t","a",
		"c","v","i","e",
	}
}


func At(board []string, x int, y int) (string) {
	return board[x+y*BOARD_SIZE]
}


func Solve([BOARD_LEN]string) ([]string) {
	return nil
} 


func main() {
	fmt.Println("Hello, 世界")
	rand.Seed(time.Now().UTC().UnixNano())

	fmt.Println(Random())
	var dict, _ = LoadDictionary()
	fmt.Println(GetPrefixWord(dict, "jeb"))



	//board := "jkdsvjkawoiqw"
}