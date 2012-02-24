//
//  Dictionary.h
//  boggle-solve-objc-xcode
//
//  Created by Chris Wilcox on 8/18/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import "NDTrie.h"


@interface Dictionary : NSObject {
	
@private
	NSMutableDictionary* dictionary;
	NDTrie* trie;
}

- (BOOL) checkWord: (NSString*)word;
- (int) countl;
- (NSArray*) checkPrefix: (NSString*)prefix;
- (NSArray*) checkSuffix: (NSString*)suffix;
- (NSArray*) checkSnippet: (NSString*)snippet;

+ (void) fromFile: (NSString*)filename;
+ (void) load: (NSString*)filename;

@end