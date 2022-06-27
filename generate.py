from typing import List, Dict, Tuple, Optional
import copy
import random
import numpy as np
import argparse


def read_words(wordlist_fp: str) -> List[str]:
    list_ = []
    with open(wordlist_fp, 'r') as f:
        for line in f.readlines():
            list_.append(line.strip())
    list_ = list(set([token.upper() for token in list_ if len(token) >= 3]))
    return list_


def works(
    s: str,
    assignment_list: List[int],
    assignment_dict: Dict[str, int],
    side_assignments: Dict[int, List[str]],
) -> Optional[Dict[int, List[str]]]:
    # note: expects the assignment list, assignment_dict, side_assignments
    # to each have nonzero length already.

    # no letters left means it works.
    if len(s) == 0:
        return side_assignments

    # letters are always assigned to exactly one side.
    if s[0] in assignment_dict:
        al = copy.deepcopy(assignment_list)
        ad = copy.deepcopy(assignment_dict)
        sa = copy.deepcopy(side_assignments)
        side_id = assignment_dict[s[0]]
        al.append(side_id)
        return works(
            s=s[1:], assignment_list=al, assignment_dict=ad, side_assignments=sa
        )

    for side_id in range(4):
        # consecutive letters cannot be assigned to the same side.
        if side_id == assignment_list[-1]:
            continue
        # only three letters can only be assigned to a side.
        if side_id in side_assignments and len(side_assignments[side_id]) == 3:
            # since the current letter wasn't in the assignment dict earlier
            # it can't be in side_assignments[side_id], so if this has len 3,
            # it can't be on this side.
            continue

        # since there's nothing immediately preventing the current letter from being
        # assigned this side id, we continue our depth-first search.
        al = copy.deepcopy(assignment_list)
        ad = copy.deepcopy(assignment_dict)
        sa = copy.deepcopy(side_assignments)
        al.append(side_id)
        ad[s[0]] = side_id
        if side_id not in sa:
            sa[side_id] = []
        sa[side_id].append(s[0])
        sa_new = works(
            s=s[1:], assignment_list=al, assignment_dict=ad, side_assignments=sa
        )
        if sa_new is not None:
            return sa_new

    # if none of the assignment suffixes for the given assignment prefix passed in work,
    # the prefix doesn't work.
    return None


def sample(wordlist_fp: str) -> Tuple[str, str, Dict[int, List[str]]]:
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
            # without loss of generality, we can always assign the first letter to
            # the top, and then permute the side assignments before returning.
            s = w1[1:] + w2[1:]
            assignment_list = [0]
            assignment_dict = {w1[0]: 0}
            side_assignments = {0: [w1[0]]}
            sa_new = works(
                s=s,
                assignment_list=assignment_list,
                assignment_dict=assignment_dict,
                side_assignments=side_assignments,
            )
            if sa_new is not None:
                return w1, w2, permute_sides(sa_new)
    raise ValueError("Couldn't find any combo with the given wordlist.")


def permute_sides(side_assignments: Dict[int, List[str]]) -> Dict[int, List[str]]:
    sp = np.random.permutation(4).tolist()
    psa = {}
    for side_id in range(4):
        new_side_id = sp[side_id]
        ip = np.random.permutation(3).tolist()
        items = []
        for i in range(3):
            items.append(side_assignments[side_id][ip[i]])
        psa[new_side_id] = items
    return psa


def render(side_assignments: Dict[int, List[str]]) -> None:
    shift = "".join([" "] * 40)
    print()
    print(shift + '   ' + '   '.join(side_assignments[0]) + '   ')
    print()
    for i in range(1, 6):
        if i % 2 == 1:
            print(
                shift + side_assignments[1][i // 2] +
                '             ' +
                side_assignments[2][i // 2]
            )
        else:
            print()
    print()
    print(shift + '   ' + '   '.join(side_assignments[3]) + '   ')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--wordlist_fp', type=str, default='words.txt')
    args = parser.parse_args()

    w1, w2, side_assignments = sample(args.wordlist_fp)
    render(side_assignments)

    print_answer = input("\ngive up? [y/N]: ")
    if print_answer.lower() == 'y':
        print(' '.join([w1, w2]))
