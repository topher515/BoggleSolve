//
//  Board.h
//  boggle-solve-objc-xcode
//
//  Created by Chris Wilcox on 8/18/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import <Cocoa/Cocoa.h>

#define MIN_WORD_LENGTH 3
#define BOARD_SIZE 4

@interface Board : NSObject {
	NSArray *dice;
	NSArray *board;
}

- (NSString *) description;
- (id) initWithString:(NSString *)boardString;
- (id) initWithArray:(NSArray *)boardArray;
- (id) initRandom;
- (NSString *) atX:(int)x Y:(int)y;
+ (id) boardRandom;

@end
