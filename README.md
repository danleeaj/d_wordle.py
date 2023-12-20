# d_wordle.py

#### Video Demo: <https://youtu.be/J6ir7AMcLWw>

This program was created by [danleeaj](https://github.com/danleeaj) for the CS50P Final Project. Third-party libraries used include: [pyfiglet](https://pypi.org/project/pyfiglet/) and [termcolor](https://github.com/termcolor/termcolor). This is a clone of Wordle, a word guessing game in which the user is provided with feedback of whether the letter they guessed was right and whether it was at the correct position after each guess. In addition to implementing the feedback functionality, a save function was also implemented, where correct guesses and the corresponding number of guesses is stored in a .csv file. If the same user returns and enters the same username, that savefile is loaded to prevent the user from getting the same word twice. A difficulty level is also implemented that can only be changed at the command-line (details described below). Finally, the game can be closed at anytime using ^D, or ^C (but that isn't recommended because that is accompanied by a lot of unappealing error messages). Upon quitting the game, the user is presented with their guess distribution, where they can see how many guesses they used before they reached their final, correct answer.

## command line arguments:
The program takes two arguments:
* **difficulty** (-d) sets the difficulty of the game. There are 3 difficulties, and each difficulty results in a different wordlist to be fetched where the solution will be obtained from.
* **username** (-u) sets the username for the current user. A save file will be created and named after this username. The username only takes alphanumerical characters and no spaces. The username must also be less than 12 characters. If a savefile already exists for this username, the program will read the user's corresponding file.

## wordlists:
Wordlists were taken from online sources:
* [**easy**](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/TV/2006/1-1000) was taken from the top 3000 words used in television and movies. The words in this list were downloaded by saving the page as a .html. A Python script was written to scrub through the list using regular expressions to extract 5 letter alphabetical words, and wrote those words to a new .txt file, totalling up to 613 words.
* [**regular**](https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b) consists of all historical Wordle solutions, totalling up to 2317 words.
* [**hard**](https://gist.github.com/cfreshman/cdcdf777450c5b5301e439061d29694c) consists of all possible 5-letter word combinations, as per Wordle's allowed guesses, totalling up to 12972 words. This is also the list that will be used to determine whether a user input is allowed.

## savefiles

A unique take this version of d_wordle implemented is the use of local saves. Whenever a username is inputted, either in the command line or if prompted in the beginning of the program, the os package is called to see if the user already exists. If not, a file named {username}.csv is created within the "/save" directory. Within this save file, two columns are saved: the word (if guessed correctly), and the number of guesses it took. This save function occurs at the end of every round only if the word has been guessed correctly. If the savefile is found after user input, the wordlist found within is stored in a new list called completed_wordlist. Everytime a random word is chosen from the wordlist of the corresponding difficulty, it is compared to the words in the completed_wordlist. If there is a match, the random selection processes is repeated until it finds a unique word the user has not gotten correct yet.

## other dependencies

In a folder called data exists all my wordlists based on difficulty. In a folder called saves exists all my save files, which should be empty as I submit this assignment.

# the game process

First, the game is initialized. Upon initialization, a word is randomly selected, cross-checked with the user's completed wordlist, and stored in the solution variable. The program then prompts the user to enter a 5 letter guess, which must also be cross-checked with the possible answers word list (sol.txt) to see if it is an existing word. This is important because this prevents the user from exploiting the game by trying the most common letters via made up words. Once the input is validated, the assign fucntion is used to make both strings (the solution and the input) into a dictionary, which details what each corresponding character is. For example, the word 'hello' becomes {1: 'h', 2: 'e', 3: 'l', 4: 'l', 5: 'o'}. Then, these are compared in the compare function which compares each letter, in order, in both the solution and the input. The compare function also creates a set that contains all letters found in the solution. Then, the input is compared to the set to see if the letters in the input are found in the solution. This function returns a dictionary. This new dictionary returns each letter in the input, and whether the letter a) is in the right place, b) is found in the solution but not in the right place, or c) not found in the solution. This is then sent to a function called printo which uses the case match functionality to, depending on the "correctness" of each letter, prints it in its original color, on the yellow or a green backdrop. At the same time, the compare function is also keeping score for each match. A complete match, which results in a score of 5, will cause an while True loop inside the main function to break, which signifies the end of the round.

## guess distribution

At the end of the game, when the user quits via ^D, a guess distribution is shown. This is achieved using a score() function which takes the existing scores found within the user's save file and converts them to a dictionary that instead shows the distribution of scores, so {1: 5, 2: 0, ... } would mean the user guessed 5 words with just one guess (what!?) and 0 words with 2 guesses, etc. This is then used to print hashes which signify the number of guesses. As I am typing this, I realize that once the user plays this game more than a hundred times, there might be some slight overflowing of hashes, however, I am pretty certain that no one will do this, so I will just leave this functionality as is.

## problems encountered

This took so much longer than I expected, almost 3 entire days of staring down VSCode and various documentation. There were a few hard pivots I made during this process. For example, I originally had dictionaries set up for comparison like so {"h": "correct", "e": "wrong position", "l": "wrong", ...} While testing, I did not find any issues with this because I did not use any words with repeating characters. I was dumbfounded when I typed in "hello" for fun, and received a dictionary of length 4. This is because dictionaries do not support multiple, repeating keys, because what is the purpose of a key if they are not unique. I tackled this issue by altering the format of the return compare dictionary so that instead of a single dictionary, it is a list of 5 dictionaries, each detailing the order, the letter and the correctness. Another major issue I encountered was at the end, right before submitting this assignment. Because I was not confident in object-oriented programming, I wanted to torture myself by making as many as my functions nested within a class. After I finished programming the game, I went to check the submission requirements and realized that my functions should be at the same level as main(). So I had to redo parts of my script to take the classmethods and functions that I found to be integral to the program, out of the Game class.

All in all, I really enjoyed making d_wordle.py, and I **really** enjoyed taking CS50P. I took this course as a break from CS50x (shoutout to tideman), but I think I am ready to go back.

See you in the CS50x final project!

This was d_wordle.py.
