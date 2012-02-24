#import <Foundation/Foundation.h>
#import "Dictionary.h"
#import "Board.h"
#import "BoggleSolver.h"


int main (int argc, const char * argv[]) {
    NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];

	/*FOUNDATION_EXPORT BOOL NSZombieEnabled;
    NSZombieEnabled = YES;*/
	
	NSString *boardString = @"";
	Board *board = nil;
	if (argc > 1) {
		boardString = [NSString stringWithCString:argv[1] encoding:NSASCIIStringEncoding];
		if (boardString.length != 16) {
			NSLog(@"Invalid board: %@. Must be 16 characters.", boardString);
			return 1;
		}
		@try {
			board = [[Board alloc] initWithString:boardString];
		}
		@catch (NSException *e) {
			NSLog(@"Invalid board: %@", boardString);
			return 1;
		}
	} else {
		board = [[Board alloc] initRandom];
	}
	
	NSLog(@"Using board:\n%@\n", board);
	
	BoggleSolver *solver = [[BoggleSolver alloc] init];
	NSArray *solutions = [solver solve:board];
	NSLog(@"Solutions: %@", solutions);
	
    // free memory
	[board release];
	
    [pool drain];
    return 0;
}
