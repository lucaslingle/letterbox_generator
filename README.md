# letterbox_generator
Generate NYT-style ['Letter Boxed'](https://www.nytimes.com/puzzles/letter-boxed) games!

### Usage

We require python version >= 3.5. To generate a puzzle, simply run
```
python3 generate.py
```

### Technical details

All our puzzles are built with a solution in two words. The generator script uses recursion and backtracking, in the style of depth-first search, 
to perform the necessary checks and assignments of letters to word box sides. 
Search and assignments are performed in such a way that every valid layout for a given word pair is equally likely. 

Our wordlist is based on the one from the [google-10000-english repo](https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt), 
but with person names, organization names, locations, nationalities, ethnicities, religions, abbreviations, molecular names, astronomical names, trademarked names, and recent loanwords removed, similar to the NYT wordlist. 
Using this script, most puzzles take less than one second to generate, and in our experience always take less than ten seconds.  

To provide your own wordlist, run ```python3 generate.py --wordlist_fp=PATH_TO_WORDLIST```.

