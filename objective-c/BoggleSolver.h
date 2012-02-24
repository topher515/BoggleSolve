//
//  BoggleSolver.h
//  boggle-solve-objc-xcode
//
//  Created by Chris Wilcox on 8/18/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import "Dictionary.h"
#import "Board.h"

@interface BoggleSolver : NSObject {
	Dictionary *dict;
	NSArray *lastSolution;
	Board *lastBoard;
}

- (NSArray *) solve: (Board *)board;

@end
