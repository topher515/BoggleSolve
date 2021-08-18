package main

import (
	"bufio"
	"bytes"
	"errors"
	"fmt"
	"math/rand"
	"os"
	"sort"
	"strings"
	"time"
)

const (
	BOARD_SIZE   = 4
	BOARD_LEN    = BOARD_SIZE * BOARD_SIZE
	DICT_PATH    = "/usr/share/dict/words"
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

type Coord struct {
	x int
	y int
}

/// Stack ///

type Stack struct {
	top  *Element
	size int
}

type Element struct {
	value interface{}
	next  *Element
}

// Return the stack's length
func (s *Stack) Len() int {
	return s.size
}

// Push a new element onto the stack
func (s *Stack) Push(value interface{}) {
	s.top = &Element{value, s.top}
	s.size++
}

// Remove the top element from the stack and return it's value
// If the stack is empty, return nil
func (s *Stack) Pop() (value interface{}) {
	if s.size > 0 {
		value, s.top = s.top.value, s.top.next
		s.size--
		return
	}
	return nil
}

/// END STACK ///

func LoadDictionary() ([]string, error) {
	var words = []string{}
	var fp, err = os.Open(DICT_PATH)
	if err != nil {
		panic(err)
	}
	var reader = bufio.NewReader(fp)

	var word = ""
	for ; err == nil; word, err = reader.ReadString('\n') {
		if len(word) < WORD_MIN_LEN {
			continue
		}
		words = append(words, strings.Trim(word, " \n\r\t"))
	}
	sort.Strings(words)

	return words, nil
}

func GetPrefixWord(dict []string, prefix string) (string, error) {
	var index = sort.Search(len(dict), func(i int) bool {
		return bytes.Compare([]byte(dict[i]), []byte(prefix)) >= 0

	})
	if index < len(dict) && len(prefix) <= len(dict[index]) {
		if dict[index][0:len(prefix)] == prefix {
			return dict[index], nil
		}
	}
	return "", errors.New("No prefix found")
}

func Random() [BOARD_LEN]string {

	// Roll the dice
	for i := range dice {
		j := rand.Intn(i + 1)
		dice[i], dice[j] = dice[j], dice[i]
	}

	// Build a new board
	var board = [BOARD_LEN]string{}
	for i, die := range dice {
		var x = rand.Intn(6)
		board[i] = die[x : x+1]
	}
	return board
}

func Predefined() [BOARD_LEN]string {
	return [BOARD_LEN]string{
		"s", "e", "w", "y",
		"p", "l", "e", "x",
		"a", "t", "t", "a",
		"c", "v", "i", "e",
	}
}

func At(board [BOARD_LEN]string, x int, y int) string {
	return board[x+y*BOARD_SIZE]
}

func SolveRecurse(dict []string, board [BOARD_LEN]string, x int, y int, current string, touched *map[Coord]bool, wordChan *chan string) {

	if x < 0 || x >= BOARD_SIZE {
		return
	}
	if y < 0 || y >= BOARD_SIZE {
		return
	}

	current = current + At(board, x, y)

	if len(current) == 1 {
		// Dont even bother looking at prefixes for len(1) words
	} else if len(current) > 1 {
		possibleWord, err := GetPrefixWord(dict, current)
		//fmt.Println(current)
		//fmt.Println(possibleWord)
		if err != nil {
			return
		}
		if possibleWord == current {
			(*wordChan) <- possibleWord
			//(*found)[possibleWord] = true
		}
	} else { // Current == 1
		panic("Sheet guys")
	}

	var coord Coord
	coord.x = x
	coord.y = y

	(*touched)[coord] = true

	for i := -1; i <= 1; i++ {
		for j := -1; j <= 1; j++ {
			var nextCoord Coord
			nextCoord.x = x + i
			nextCoord.y = y + j
			if (*touched)[nextCoord] {
				continue
			}
			SolveRecurse(dict, board, nextCoord.x, nextCoord.y,
				current, touched, wordChan)
		}
	}

	(*touched)[coord] = false
	//fmt.Println(current)
	current = current[0:len(current)]
}

func StartSolveRoutine(dict []string, board [BOARD_LEN]string, x int, y int, wordChan *chan string) {
	touched := make(map[Coord]bool)
	SolveRecurse(dict, board, x, y, "", &touched, wordChan)
	close(*wordChan)
}

func Solve(dict []string, board [BOARD_LEN]string) []string {

	foundList := []string{}
	wordChans := []chan string{}

	// Start a goroutine for each letter on the board
	for x := 0; x <= BOARD_SIZE; x++ {
		for y := 0; y <= BOARD_SIZE; y++ {
			wordChan := make(chan string, 100)
			go StartSolveRoutine(dict, board, x, y, &wordChan)
			wordChans = append(wordChans, wordChan)
		}
	}

	// Keep checking word channels until they're all closed
	// append foundWords as they're found
	for {
		allClosed := true
		for _, wordChan := range wordChans {

			foundWord, ok := <-wordChan
			if ok {
				foundList = append(foundList, foundWord)
				allClosed = false
			}
		}
		if allClosed {
			break
		}
	}

	return foundList
}

func main() {

	board := [BOARD_LEN]string{}

	dict, _ := LoadDictionary()

	// TODO: Support args eventually
	// if len(os.Args) > 1 {
	// 	copy(board[:], os.Args[1:][:])
	// } else {
	// ...
	// }

	rand.Seed(time.Now().UTC().UnixNano())
	randomBoard := Random()
	copy(board[:], randomBoard[:])

	println("Solving for board: ", strings.Join(board[:], "")) // to stderr

	solved := Solve(dict, board)
	for _, x := range solved {
		fmt.Println(x)
	}

}
