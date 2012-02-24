//
//  BoggleSolver.m
//  boggle-solve-objc-xcode
//
//  Created by Chris Wilcox on 8/18/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import "BoggleSolver.h"
#import "Dictionary.h"
#import "Board.h"


void *_check( int x, int y, NSMutableString *checking, NSMutableDictionary *checked, NSMutableArray *foundWords, 
			   Board *board, Dictionary *dict) {
	NSString *l = [board atX:x Y:y];
	if (l == nil || [checked objectForKey:[NSString stringWithFormat:@"%d,%d", x,y]] != nil) {
		return nil;
	}
	
	[checked setValue:@"true" forKey:[NSString stringWithFormat:@"%d,%d", x,y]];
	[checking appendString:l]; //Push to string
	
	if ([[dict checkPrefix:checking] count] == 0) {
		[checking deleteCharactersInRange:NSMakeRange(checking.length-1, 1)]; // Pop
		[checked removeObjectForKey:[NSString stringWithFormat:@"%d,%d",x,y]];
		return nil;
	}
	
	if (checking.length >= MIN_WORD_LENGTH && [dict checkWord:checking] && !([foundWords containsObject:checking])) {
		[foundWords addObject:[NSString stringWithString:checking]];
	}
	
	for (int y_delta=-1; y_delta<=1; y_delta++) {
		for (int x_delta=-1; x_delta<=1; x_delta++) {
			_check(x+x_delta,y+y_delta,checking,checked,foundWords,board,dict);
		}
	}
	
	[checked removeObjectForKey:[NSString stringWithFormat:@"%d,%d",x,y]];
	[checking deleteCharactersInRange:NSMakeRange(checking.length-1, 1)]; // Pop
	return nil;
	
}


@implementation BoggleSolver

- (id) init {
	if ((self = [super init]) != nil) {
		dict = [[Dictionary alloc] init];
	}
	return self;
}


- (NSArray *) solve: (Board *)board  {
	
	lastBoard = board;
	
	NSMutableArray *foundWords = [[NSMutableArray alloc] init];
	NSMutableDictionary *checked = [[NSMutableDictionary alloc] init];
	NSMutableString *checking = [[NSMutableString alloc] init];
	
	for (int x = 0; x<BOARD_SIZE; x++) {
		for (int y = 0; y<BOARD_SIZE; y++) {
			_check(x,y,checking,checked,foundWords,board,dict);
		}
	}
	
	lastSolution = [NSArray arrayWithArray:foundWords];
	[foundWords release];
	[checked release];
	[checking release];
	return lastSolution;
	
}

@end


