import os
import ntpath
import linecache
import string
import dpath.util


search_dict={}
file_list={}
letter_list = list(string.ascii_lowercase)

class AutoCompleteData:
    def __init__(self, full_str, term, source, num_line, score):
        self.completed_sentence = full_str
        self.source_text = f"{ntpath.basename(source)[:-4]} {num_line}"
        full_str_lower = full_str.lower()
        #self.offset = full_str_lower.find(term)
        self.score = score

    def print(self):
        print(f"complete sentence: {self.completed_sentence} ({self.source_text})\n")

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

def k_top(term_list,k = 5):
    if (len(term_list)) <= k:
        return term_list
    return_list = []
    min_list = []
    term_list.sort(key=lambda tup: tup[3], reverse=True)
    i = 0
    print(term_list[i][3])
    print(term_list[k-1][3])
    while (i < len(term_list)) and (term_list[i][3] > term_list[k-1][3]):
        return_list.append(term_list[i])
        i += 1

    while (i < len(term_list)) and (term_list[i][3] == term_list[k-1][3]):
        min_list.append(term_list[i])
        i += 1
    min_list = sorted(min_list, key=lambda tup: tup[0].casefold())[:k - len(return_list)]
    return_list += min_list
    return return_list

def is_in_dict(term, new_term, score):
    list = []
    tmp = search_dict.get(new_term)
    if (tmp != None):
        for tup in tmp:
            line = linecache.getline(file_list[tup[0]], tup[1])[:-1]
            if term != new_term:
                if term not in line:
                    list.append(tuple([line, tup[0], tup[1], score]))
            else:
                list.append(tuple([line, tup[0], tup[1], score]))
    return list


def check_switch(term):
    switch_list = []
    #print("in switch function:")
    for i in range(len(term)):
        for letter in letter_list:
            if (letter != term[i]):
                new_term = term[:i] + letter + term[i+1:]
                switch_list += is_in_dict(term, new_term, calculate_score("switch", len(term), i))

    #print("switch list - before: ")
    #print(switch_list)

    switch_list = k_top(switch_list)
    print("switch list - after: ")
    print(switch_list)
    return switch_list

def check_extra(term):
    extra_list = []
    #print("in extra function:")
    for i in range(len(term)):
        new_term = term[:i] + term[i+1:]
        extra_list += is_in_dict(term, new_term, calculate_score("extra", len(term), i))

    #print("extra list - before: ")
    #print(extra_list)

    extra_list = k_top(extra_list)
    print("extra list - after: ")
    print(extra_list)
    return extra_list

def check_missing(term):
    missing_list = []
    #print("in missing function:")
    for i in range(len(term)+1):
        for letter in letter_list:
            new_term = term[:i] + letter + term[i:]
            missing_list += is_in_dict(term, new_term, calculate_score("missing", len(term), i))

    #print("missing list - before: ")
    #print(missing_list)

    missing_list = k_top(missing_list)
    print("missing list - after: ")
    print(missing_list)
    return missing_list

def check_perfect(term):
    perfect_list = is_in_dict(term, term, calculate_score("perfect", len(term), -1))

    #print("perfect list - before: ")
    #print(perfect_list)

    perfect_list = k_top(perfect_list)
    print("perfect list - after: ")
    print(perfect_list)
    return perfect_list



def init(file_path):
    file_index=-1
    for root, dirs, files in os.walk(file_path):
        for name in files:
            file_index+=1
            file_list[file_index]=os.path.abspath(os.path.join(root, name))
            file = open(os.path.abspath(os.path.join(root, name)), "r", encoding="utf8")
            num_line = 0
            for line in file:
                num_line += 1
                line = line[:-1]
                for i in range(len(line)):
                    min_len = min(len(line), i+10)
                    for j in range(i + 3, min_len+1):
                        word = line[i:j].lower()
                        if word not in search_dict.keys():
                            search_dict[word] = []
                        search_dict[word].append(tuple([file_index, num_line]))

    #print(file_list)
    #print(search_dict)




def search(term):
    term = term.lower()
    perfect_list = check_perfect(term)
    switch_list = check_switch(term)
    missing_list = check_missing(term)
    extra_list = check_extra(term)

    term_list = perfect_list + switch_list + missing_list + extra_list

    term_list = k_top(term_list)

    #print("SEARCH: ")
    #print(term_list)

    return_list = []
    for item in term_list:
        return_list.append(AutoCompleteData(item[0], term, file_list[item[1]], item[2], item[3]))
    return return_list


init("./some_files")
res = search("function")

for i in res:
    i.print()

