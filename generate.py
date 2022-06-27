from typing import List, Dict, Tuple, Optional
import copy
import random
import numpy as np
import argparse

count = 0


def has_contiguous_repeat(w: str):
    for i in range(0, len(w) - 1):
        if w[i] == w[i + 1]:
            return True
    return False


def read_words(wordlist_fp: str) -> List[str]:
    list_ = []
    with open(wordlist_fp, "r") as f:
        for line in f.readlines():
            list_.append(line.strip())
    set_ = {w.upper() for w in list_ if len(w) >= 3 and not has_contiguous_repeat(w)}
    return list(set_)


def search(
    s: str,
    state: Dict[str, int],
    last_side_id: int,
) -> Optional[Dict[str, int]]:
    """
    Performs search, assigning the letters of s to possible positions.
    If a successful layout for the entire string is found, it will be returned.

    :param s: String suffix yet to be assigned to sides.
    :param state: Dictionary mapping from characters to positions 0, ..., 11.
    :param last_side_id: Side ID assigned to previous character.
    :return: Final layout state or None.
    """
    global count
    count += 1

    # no letters left means it works.
    if len(s) == 0:
        return state

    # check if s[0] was seen earlier and thus already assigned somewhere.
    if s[0] in state:
        pos_id = state[s[0]]
        side_id = pos_id // 3
        # if this forced assignment causes the new letter to fall on the same side
        # as the previous letter, we have a problem.
        if side_id == last_side_id:
            return None
        return search(
            s=s[1:],
            state=copy.deepcopy(state),
            last_side_id=side_id,
        )

    # s[0] is a newly-seen character, so we assign it uniformly at random to any
    # open position that works, if there are any.
    blanks = set(range(12)) - (set(state.values()))
    blanks = list(blanks)
    random.shuffle(blanks)
    for pos_id in blanks:
        side_id = pos_id // 3
        # consecutive letters cannot be assigned to the same side.
        if side_id == last_side_id:
            continue
        # only three letters can only be assigned to a side.
        if len([k for k, v in state.items() if v // 3 == side_id]) == 3:
            continue

        # since there's nothing immediately preventing s[0] from being
        # assigned this position id, we continue our depth-first search.
        state_new = copy.deepcopy(state)
        state_new[s[0]] = pos_id
        final_state = search(
            s=s[1:],
            state=state_new,
            last_side_id=side_id,
        )
        if final_state is not None:
            return final_state

    # if none of the assignment suffixes for the given assignment prefix passed in work,
    # the prefix doesn't work.
    return None


def sample(wordlist_fp: str, verbose: bool) -> Tuple[str, str, Dict[str, int]]:
    w1list = read_words(wordlist_fp)
    w2list = copy.deepcopy(w1list)

    random.shuffle(w1list)
    random.shuffle(w2list)
    for w1 in w1list:
        for w2 in w2list:
            if w1[-1] != w2[0]:
                continue
            if len(set(w1 + w2)) != 12:
                continue
            if verbose:
                print(w1, w2)
            # we assign the first letter uniformly at random to any position.
            pos_id = np.random.randint(0, 12)
            side_id = pos_id // 3
            final_state = search(
                s=w1[1:] + w2[1:], state={w1[0]: pos_id}, last_side_id=side_id
            )
            if final_state is not None:
                return w1, w2, final_state
    raise ValueError("Couldn't find any combo with the given wordlist.")


def render(final_state: Dict[str, int]) -> None:
    shift = "".join([" "] * 40)
    north = [k for k, v in final_state.items() if v // 3 == 0]
    east = [k for k, v in final_state.items() if v // 3 == 1]
    south = [k for k, v in final_state.items() if v // 3 == 2]
    west = [k for k, v in final_state.items() if v // 3 == 3]
    print()
    print(shift + "   " + "   ".join(north) + "   ")
    print()
    for i in range(1, 6):
        if i % 2 == 1:
            print(shift + west[i // 2] + "             " + east[i // 2])
        else:
            print()
    print()
    print(shift + "   " + "   ".join(south) + "   ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--wordlist_fp", type=str, default="words.txt")
    parser.add_argument("--verbose", type=int, choices=[0, 1], default=0)
    args = parser.parse_args()

    w1, w2, side_assignments = sample(args.wordlist_fp, verbose=bool(args.verbose))
    render(side_assignments)
    if bool(args.verbose):
        print(count)

    print_answer = input("\nShow answer? [y/N]: ")
    if print_answer.lower() == "y":
        print(" ".join([w1, w2]))
