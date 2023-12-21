import argparse
import sys
from pyfiglet import Figlet
import textwrap
import random
from termcolor import cprint
import csv
import os

class Game:

    wordlist = []
    possible_answers = [word.rstrip().lower() for word in open("words/sol.txt", "r")]
    completed_wordlist = []

    def __init__(self):
        self.solution = self.get_solution()

    def __str__(self):
        return f"{self.solution}"

    def get_solution(self):
        while True:
            selection = random.choice(self.wordlist)
            if selection not in self.completed_wordlist:
                return selection.lower()

    @classmethod
    def printo(cls, d):
        for i in range(len(d)):
            match d[i]['color']:
                case 'yellow':
                    cprint(d[i]['letter'].upper(), on_color="on_yellow", end="")
                case 'green':
                    cprint(d[i]['letter'].upper(), on_color="on_green", end="")
                case _:
                    print(d[i]['letter'].upper(), end="")
        print()

    @classmethod
    def load(cls, i):
        file = f"words/{i}.txt"
        with open(file) as file:
            for words in file:
                cls.wordlist.append(words.rstrip())

    @classmethod
    def load_save(cls, name):
        file = f"save/{name.rstrip().lower()}.csv"
        with open(file) as file:
            reader = csv.DictReader(file)
            for row in reader:
                cls.completed_wordlist.append(row['word'])

    @classmethod
    def score(cls, name):
        file = f"save/{name.rstrip().lower()}.csv"
        scores = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        with open(file) as file:
            reader = csv.DictReader(file)
            for row in reader:
                s = int(row['points'])
                scores[s] = scores[s] + 1
        print(f"Guess distribution:\n")
        for i in scores:
            print(f"{i}: " + "#" * scores[i])
        print()

    @classmethod
    def save(cls, word, name, points):
        file = f"save/{name.rstrip().lower()}.csv"
        with open(file, 'a') as file:
            fieldnames = ['word', 'points']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({'word': word, 'points': points})

class colors:
    '''
    Class used to color words to hint the user.
    '''
    RED = '\033[31m'
    GRE = '\033[32m'
    YEL = '\033[33m'
    BLU = '\033[34m'
    END = '\033[0m'

def main():

    directory = "save"
    if not os.path.exists(directory):
        os.makedirs(directory)

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", default=1, help="game difficulty [0, 1, 2 = easy, regular, hard]")
    parser.add_argument("-u", default=None, help="username (alphanumeric only, max 12 characters)")
    args = parser.parse_args()

    try:
        match int(args.d):
            case 0 | 1 | 2:
                wordlist = Game.load(args.d)
            case _:
                sys.exit("Please select a difficulty of 0, 1, or 2. See -h for help.")
    except ValueError:
        sys.exit("Please select a difficulty of 0, 1, or 2. See -h for help.")

    difficulty = int(args.d)

    if args.u == None:
        username = validate_username()
    elif args.u.isalnum() == False:
        sys.exit("Your username must be alphanumeric. See -h for help.")
    elif len(args.u) > 12:
        sys.exit("Your username must be less than 12 characters. See -h for help.")
    else:
        username = args.u.lower()

    directory = f"save/{username.lower()}.csv"
    if os.path.exists(directory):
        print(f"\n Hi, {username.upper()}, WELCOME BACK TO...")
        Game.load_save(username)
    else:
        print(f"\n Hi, {username.upper()}, WELCOME TO...")
        file = f"save/{username.rstrip().lower()}.csv"
        with open(file, 'a') as file:
            fieldnames = ['word', 'points']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    print(fancy("d_wordle.py"))

    printw(f"This is a project based on Josh Wardle's WORDLE created for CS50P. You will be given 5 opportunities to guess a random 5-letter word selected from a pool of {intro(difficulty)}.")
    printw("You may leave the game anytime by pressing control-D")

    if input("Press enter to continue. Input help for help: ").lower() == "help":
        print()
        printw("Your answer will be rejected if a) it consists of anything other than alphabets, b) it is not 5 letters long, and c) it is not an actual word.")
        printw("Once your answer is accepted, you will receive feedback via the form of colors.")
        print(f"{colors.GRE}GREEN{colors.END} means the correct letter at the correct position.")
        print(f"{colors.YEL}YELLOW{colors.END} means the correct letter at the wrong position.")
        print("COLORLESS means the letter does not appear in this word.\n")
        printw(f"For example, take 'HELLO' as an example solution. The answer 'EARTH' will result in an output of '{colors.YEL}E{colors.END}ART{colors.YEL}H{colors.END}' since, even though 'E' and 'H' exist in the word, they are not at their respective positions.")
        printw(f"However, an input of 'SHELL' will result in an output of 'S{colors.YEL}HE{colors.END}{colors.GRE}L{colors.END}{colors.YEL}L{colors.END}' since the first 'L' is at the correct position, while everything else is displaced.")
        printw(f"Finally, inputting 'HARSH' will result in the output of '{colors.GRE}H{colors.END}ARS{colors.YEL}H{colors.END}'. This means the first 'H' is in the correct position. But does not necessarily mean there exists another 'H'. The fifth 'H' being highlighted yellow just means 'H' exists in the solution.")
    else:
        print()
        pass

    round = 1

    while True:

        try:

            game = Game()

            print(f"ROUND: {round}\n")

            for i in range(5):
                answer = get_answer()
                output, score = compare(game.solution, answer)
                Game.printo(output)
                if score == 5:
                    print(f"\nCongratulations! The word was: {game.solution.upper()}\n")
                    Game.save(game.solution, username, i + 1)
                    Game.completed_wordlist.append(game.solution)
                    break

            if not score == 5:
                print(f"\nThe word was: {game.solution.upper()}\n")

            print(f"--------------------------------------------------------------\n")

            round += 1

        except (EOFError, KeyboardInterrupt):

            print(f"\n--------------------------------------------------------------\n")
            printw(f"Thanks for playing! Your progress will be saved so you won't get repeat words in future attempts.\n")

            game.score(username)

            break

def compare(solution, s):

    score = 0

    results = []

    letters = set()

    ans = assign(s.lower())
    sol = assign(solution.lower())

    for i in range(len(sol)):
        letters.add(sol[i])

    for i in range(len(sol)):
        d = {}
        d["order"] = i
        d["letter"] = ans[i]
        if ans[i] == sol[i]:
            d["color"] = "green"
            score = score + 1
        elif ans[i] in letters:
            d["color"] = "yellow"
        else:
            d["color"] = None
        results.append(d)

    return results, score

def validate(s):
    for word in Game.possible_answers:
        if word == s.rstrip().lower():
            return True
    return False

def assign(s):
    a = {}
    for i, c in enumerate(s):
        a[i] = c
    return a

def fancy(s):
    '''
    This function "fancifies" the string sent to it and returns an ASCII text version using the pyfiglet library.
    '''
    f = Figlet(font='slant')
    return f.renderText(s)

def printw(s):
    wrapper = textwrap.TextWrapper(width=61)
    rows = wrapper.wrap(text=s)
    for row in rows:
        print(row)
    print()

def validate_username():
    while True:
        s = input("Username: ")
        if s == None:
            print("Please enter a username.")
        elif s.isalnum() == False:
            print("Your username must be alphanumeric.")
        elif len(s) > 12:
            print(f"Your username must be a maximum of 12 characters. Current: {len(s)}")
        else:
            return s.lower()

def intro(i):
    match i:
        case 0:
            return("the most commonly used words in television and movies")
        case 1:
            return("previous New York Times' Wordle solutions")
        case 2:
            return("all possible words, as per New York Times' Wordle's accepted inputs")

def get_answer():
    while True:
        try:
            answer = input()
            if validate(answer) == True:
                return answer
            raise ValueError
        except ValueError:
            cprint("Invalid answer", on_color="on_red")

if __name__ == "__main__":
    main()
