//
//  Dictionary.m
//  boggle-solve-objc-xcode
//
//  Created by Chris Wilcox on 8/18/10.
//  Copyright 2010 __MyCompanyName__. All rights reserved.
//

#import "Dictionary.h"


@implementation Dictionary

- (id) init {
	if (self = [super init]) {
		
		NSLog(@"Building dictionary from '/usr/share/dict/words'");
		
		NSError *error;
		NSString *stringFromFile = [[NSString alloc]
									initWithContentsOfFile:@"/usr/share/dict/words"
									encoding:NSUTF8StringEncoding
									error:&error ];
		
		NSMutableArray *wordsArray = [[NSMutableArray alloc] init];
		
		for (NSString *word in [stringFromFile componentsSeparatedByString:@"\n"]) {
			if (!([word isEqualToString:@""]) && [[word substringToIndex:1] isEqualToString: [[word substringToIndex:1] lowercaseString]]) {
				[wordsArray addObject:word];
			} 
		}
		
		trie = [NDTrie trieWithArray:wordsArray];
		
		[stringFromFile release];
		[wordsArray release];
	}
	return self;
}

- (BOOL) checkWord: (NSString *)word {
	//NSLog(@"Checking word: '%@'", word);
	BOOL found = [trie containsString:word];
	return found != nil;
}

- (NSArray *) checkPrefix:(NSString *)prefix {
	//NSLog(@"Checking prefix: '%@'", prefix);
	if ([trie containsStringWithPrefix:prefix]) {
		return [trie everyStringWithPrefix:prefix];
	} else {
		return [[NSArray alloc] init];
	}
}

- (int) countl {
	return [trie count];
}

@end