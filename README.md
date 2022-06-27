# letterbox_generator
Generate NYT-style letterbox games!

### Usage

```
python3 generate.py
```

### Technical details

All our puzzles are built with a solution in two words. The generator script uses recursion and backtracking, in the style of depth-first search, 
to perform the necessary checks and assignments of letters to word box sides. 

Our wordlist is based on the one from the [google-10000-english repo](https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt).
Different from the NYT word list, this list includes the names of geographic locations and some abbreviations. We estimate that these show up in fewer than 5% of the puzzles.

To provide your own wordlist, run ```python3 generate.py --wordlist_fp=PATH_TO_WORDLIST```.
