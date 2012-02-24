//
//  Board.m
//  boggle-solve-objc-xcode
//
//  Created by Chris Wilcox on 8/18/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import "Board.h"


@implementation Board


- (id) init {
	if ((self = [super init]) != nil) {
		dice = [NSArray arrayWithObjects:@"iefyeh",
			@"eptslu",
			@"henips",
			@"lecars",
			@"avndze",
			@"dkunto",
			@"snedwo",
			@"tgievn",
			@"eylugk",
			@"fbirxo",
			@"bqajmo", // q is actually 'qu'
			@"aaciot",
			@"camdep",
			@"aybilt",
			@"hmosar",
			@"wirglu",
			nil];	
	}
	return self;
}

- (id) initWithString:(NSString *)boardString {
	
	if ( (self = [self init]) != nil ) {
		
		if (dice.count != boardString.length) {
			[NSException raise:@"InvalidBoard" format:@"Invalid board size: %d", boardString.length];
		}
		NSMutableArray *tempArray = [[NSMutableArray alloc] init];
		for (int i=0; i<boardString.length; i++)  {
			[tempArray addObject:[NSString stringWithFormat:@"%C", [[boardString lowercaseString] characterAtIndex:i]]];
		}
		[self initWithArray:tempArray];
		[tempArray release];
	}
	return self;
}
				 
- (id) initWithArray:(NSArray *)boardArray {
 	if ( (self = [self init]) != nil ) {
		
		if (dice.count != [boardArray count]) {
			[NSException raise:@"InvalidBoard" format:@"Invalid board size: %@", [boardArray count]];
		}
		board = [NSArray arrayWithArray:boardArray];
	}
	return self;
}
				 
- (id) initRandom {
	if ((self = [self init]) != nil) {
		NSMutableArray *tempArray = [[NSMutableArray alloc] init];
		for (NSString *die in dice) {
			int r = arc4random() % die.length;
			[tempArray addObject:[NSString stringWithFormat:@"%C", [die characterAtIndex:r]]];
		}
		[self initWithArray:tempArray];
		[tempArray release];
	}
	return self;
}
	
- (NSString *)description {
	NSMutableString *tempString = [[NSMutableString alloc] init];
	for (int i=0; i<[board count]; i++) {
		if (i % BOARD_SIZE == 0 && i != 0) {
			[tempString appendString:@"\n"];
		}
		[tempString appendString: (NSString *) [board objectAtIndex:i]];
	}
	NSString *ret = [NSString stringWithString: tempString];
	[ret retain];
	[tempString release];
	return ret;
}

- (NSString *)atX:(int)x Y:(int)y {
	if (x >= BOARD_SIZE || y >= BOARD_SIZE || x < 0 || y < 0) {
		return nil;
	}
	return [board objectAtIndex:x+BOARD_SIZE*y];
}
				 
+ (id) boardRandom {
	return [[[self alloc] initRandom] autorelease];			 
}
		
@end
