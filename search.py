import ntpath
import linecache

from init import *

letter_list = list(string.ascii_lowercase)

class AutoCompleteData:
    def __init__(self, item):
        self.completed_sentence = item[0]
        self.source_text = f"{ntpath.basename(file_list[item[1]])[:-4]} {item[2]}"
        self.offset = item[4]
        self.score = item[3]

    def print(self):
        print(f"{self.completed_sentence} ({self.source_text}) offset: {self.offset}")


def calculate_score(mistake_type, len, index):
    #switch: 1, missing: 2, extra:3
    score = len*2
    if (mistake_type == "switch") or (mistake_type == "extra"):
        score -= 2
    if (mistake_type == "switch"):
        if (index >= 4):
            score -= 1
        else:
            score -= (5 - index)
    elif (mistake_type == "missing") or (mistake_type == "extra"):
        if (index >= 4):
            score -= 2
        else:
            score -= (10 - (index*2))
    return score


def k_top(term_list, k = 5):
    if (len(term_list)) <= k:
        return term_list
    return_list = []
    min_list = []
    term_list.sort(key=lambda tup: tup[3], reverse=True)
    i = 0
    while (i < len(term_list)) and (term_list[i][3] > term_list[k-1][3]):
        return_list.append(term_list[i])
        i += 1

    while (i < len(term_list)) and (term_list[i][3] == term_list[k-1][3]):
        min_list.append(term_list[i])
        i += 1
    min_list = sorted(min_list, key=lambda tup: tup[0].casefold())[:k - len(return_list)]
    return_list += min_list
    return return_list


def get_in_dict(term, new_term, score):
    list = []
    tmp = search_dict.get(new_term)
    if (tmp != None):
        tmp = tuple(set(tmp))
        for tup in tmp:
            line = linecache.getline(file_list[tup[0]], tup[1])[:-1].lstrip()
            if term != new_term:
                if term not in line:
                    list.append(tuple([line, tup[0], tup[1], score, fix_term(line).find(new_term)]))
            else:
                list.append(tuple([line, tup[0], tup[1], score, fix_term(line).find(new_term)]))
    return list


def get_switch(term):
    switch_list = []
    for i in range(len(term)):
        for letter in letter_list:
            if (letter != term[i]):
                new_term = term[:i] + letter + term[i+1:]
                switch_list += get_in_dict(term, new_term, calculate_score("switch", len(term), i))

    switch_list = k_top(switch_list)
    return switch_list


def get_extra(term):
    extra_list = []
    for i in range(len(term)):
        new_term = term[:i] + term[i+1:]
        extra_list += get_in_dict(term, new_term, calculate_score("extra", len(term), i))

    extra_list = k_top(extra_list)
    return extra_list


def get_missing(term):
    missing_list = []
    for i in range(len(term)+1):
        for letter in letter_list:
            new_term = term[:i] + letter + term[i:]
            missing_list += get_in_dict(term, new_term, calculate_score("missing", len(term), i))

    missing_list = k_top(missing_list)
    return missing_list


def get_perfect(term):
    perfect_list = get_in_dict(term, term, calculate_score("perfect", len(term), -1))
    perfect_list = k_top(perfect_list)

    return perfect_list


def search(term):
    term = fix_term(term)
    term_list = get_perfect(term)
    if (len(term_list)<5):
        switch_list = get_switch(term)
        missing_list = get_missing(term)
        extra_list = get_extra(term)
        term_list += switch_list + missing_list + extra_list
        term_list = k_top(term_list)

    return_list = []
    for item in term_list:
        return_list.append(AutoCompleteData(item))
    return return_list