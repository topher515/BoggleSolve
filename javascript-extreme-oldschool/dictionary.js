map_if = function(array,fn,condition_fn) {

	if (typeof(condition_fn) == 'undefined' || condition_fn == null)
		condition_fn = function() { return true }

	r = []		
	for (i in array) {
		if (condition_fn(array[i]))
			r.push(fn(array[i]))
	}
	return r
}

String.prototype.startsWith = function(str) 
{return (this.match("^"+str)==str)}

/*
//+ Carlos R. L. Rodrigues
//@ http://jsfromhell.com/array/search [rev. #2]

search(vector: Array, value: Object, [insert: Boolean = false]): Integer

Do a binary search on an *ordered* array, if it's not ordered, 
the behaviour is undefined. The function can return the index of 
the searched object as well the the index where it should be inserted 
to keep the array ordered.
vector -  array that will be looked up
value - object that will be searched
insert - if true, the function will return the index where the 
value should be inserted to keep the array ordered, otherwise 
returns the index where the value was found or -1 if it wasn't found
*/
search = function(o, v, i){
    var h = o.length, l = -1, m;
    while(h - l > 1)
        if(o[m = h + l >> 1] < v) l = m;
        else h = m;
    return o[h] != v ? i ? h : -1 : h;
};


function Dictionary(word_list,allow_proper_names) {
	word_list.pop()
	if (allow_proper_names)
		var wordsList = word_list
	else {
		var wordsList = map_if(word_list,
			function(x) { return x },
			function(x) { return x[0].toUpperCase() != x[0] }
		)
	}
	
	wordsList.sort()
	var wordsSet = {};
	for (i in wordsList) {
		wordsSet[wordsList[i]] = true;
	}
	
	//print(wordsList[0])
	//print(wordsList[wordsList.length-1])
	
	this.__defineGetter__('length', function() {
		return wordsList.length
	})
	
	this.checkWord = function(word) {
		if (typeof(word) != 'string')
			word = word.join('')
		if (wordsSet[word])
			return true;
		return false;
	}
	
	this.getword = function(at) {
		return wordsList[at]
	}
	
	// Return null if this word is not a prefix or any word
	// in the dictionary, otherwise return the first found
	// word (no ordering is gauranteed).
	this.checkPrefix = function(prefix) {
		if (typeof(prefix) != 'string')
			prefix = prefix.join('')
		ins_point = search(wordsList,prefix,true)
		if (wordsList[ins_point].startsWith(prefix))
			return wordsList[ins_point]
		else
			return null
	}
	
	this.dump = function() { print(wordsList); }
}
Dictionary.fromFile = function(filename) {
	return new Dictionary(readFile(filename).split('\n'));
}
Dictionary.load = function() {
	return Dictionary.fromFile('/usr/share/dict/words')
}
this.Dictionary = Dictionary
//dict = Dictionary.load()