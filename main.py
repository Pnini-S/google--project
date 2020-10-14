from search import *

def run():
    print("Loading the files and preparing the system...")
    init("./some_files")
    print("The system is ready.")
    while True:
        term = input("Enter your text: \n")
        while term[-1]!='#':
            res = search(term)
            for i in range(len(res)):
                print(f"{i+1}.", end=" ")
                res[i].print()
            term += input(f"\u001b[38;5;28m\x1B[3m{term}\033[0m")

run()
