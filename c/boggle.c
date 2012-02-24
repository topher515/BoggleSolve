#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

/* Die */
char *dice[] = {"iefyeh",
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
"wirglu"};
int NUMBER_DICE = 16;
int DICE_SIDES = 6;


/* Board */
int Board_size = 4;
struct Board {
	char letters[16];
};

char *Board_toString(struct Board *board) {
	char *board_str;//[NUMBER_DICE+Board_size];
	board_str = (char*) malloc(NUMBER_DICE+Board_size);
	int i,j=0;
	for (i=0; i<NUMBER_DICE; i++) {
		if (i % Board_size == 0 && i != 0) {
			board_str[j] = '\n';
			j++;
		}
		board_str[j] = board->letters[j];
		j++;
	}
	board_str[j] = '\n';
	return board_str;
}

struct Board *Board_random(int seed) {
	if (seed != 0) {
		srand(seed);
	} else {
		srand((unsigned int)time(NULL));
	}
	
	int i, used_dice[NUMBER_DICE];
	memset(used_dice,0,sizeof(int)*NUMBER_DICE);
	
	struct Board *board;
	board = (struct Board*) malloc(sizeof(struct Board));
	int die_num;
	for (i=0; i<NUMBER_DICE; i++) {
		
		die_num = rand() % NUMBER_DICE;
		while (used_dice[die_num]) {
			die_num++;
			if (die_num == NUMBER_DICE) {
				die_num = 0;
			}
			//printf("%d\n", die_num); fflush(stdout);
		}
		used_dice[die_num] = 1;
		board->letters[i] = dice[die_num][random() % DICE_SIDES];
		//printf(":%s,", board->letters); fflush(stdout);
	}
	return board;
}

char *Board_at(struct Board *board, int x, int y) {
	if (x >= Board_size || y >= Board_size || x < 0 || y < 0)
		return NULL;
	char letter = board->letters[x+Board_size*y];
	
	char *ret_letters;
	if (letter == 'q') {
		ret_letters = (char*) malloc(sizeof(char)*2);
		strcpy(ret_letters,"qu");
	} else {
		ret_letters = (char*) malloc(sizeof(char));
		(*ret_letters) = letter;
		//*(ret_letters+sizeof(char)) = 'j';
	}
	return ret_letters;
}

int main(void) {
	struct Board *board = Board_random(0);
	int i;
	//printf("Boggle Solve in C");
	printf("%s", Board_toString(board));
	printf("at %d,%d: %s",1,2,Board_at(board,1,2));
}