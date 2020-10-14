import os
import string

search_dict={}
file_list={}

def fix_term(term):
    term = term.lower()
    out = term.translate(str.maketrans('', '', string.punctuation))
    i=0
    while i != len(out):
        if out[i] == " ":
            j=i
            while j<len(out) and out[j] == " ":
                j+=1
            out = out[:i+1] + out[j:]
        i+=1
    return out


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
                    min_len = min(len(line), i+20)
                    for j in range(i + 3, min_len+1):
                        word = fix_term(line[i:j])
                        if word not in search_dict.keys():
                            search_dict[word] = []
                        search_dict[word].append(tuple([file_index, num_line]))

