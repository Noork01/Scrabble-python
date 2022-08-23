# 6.0001 Problem Set 3

# The 6.0001 Word Game

# Name          : Noor Khan


import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7          # adjustable value

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}




WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq




#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters,
    or the empty string "". You may not assume that the string will only contain
    lowercase letters, so you will have to handle uppercase and mixed case strings
    appropriately.

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    wordlen = len(word)
    score = 0
    for i in range(wordlen):
        score += SCRABBLE_LETTER_VALUES[word[i].lower()]  #adds score for all letters
    score *= max(1,((7*wordlen)-(3*(n-wordlen))))         #then multiplies it by the max of 7*wordlen - 3*(n-wordlen) and 1
    return score                                          #then returns the score

    #pass  # TO DO... Remove this line when you implement this function


#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """

    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')  # print all on the same line
    print()  # print an empty line


#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand = {}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels-1):          # 1/3 - 1 letters in hand are vowels
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    hand['x'] = hand.get('*', 0) +1        # 1 letter is wildcard

    for i in range(num_vowels, n):         # rest are consonants
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured).

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """
    newhand = hand.copy()
    wordlen = len(word)
    for i in range(wordlen):
        if (newhand.get(word[i].lower(),0) > 0):          # if a letter belonging to the word is in the hand then it removes it
            newhand[word[i].lower()] -= 1                 # this updates the hand even if not all the letters belonging to the word are here

    return newhand

    #pass  # TO DO... Remove this line when you implement this function


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    inList = word.lower() in load_words()                 # checks if the word is in the word list
    if '*' in word:                                       # if the word has a wildcard, we replace it with a vowel then check if its in the wordlist
        if ((word.replace('*', 'a') in load_words()) or
            (word.replace('*', 'e') in load_words()) or
            (word.replace('*', 'i') in load_words()) or
            (word.replace('*', 'o') in load_words()) or
            (word.replace('*', 'u') in load_words())):
            inList = True

    inHand = True
    newhand = hand.copy()
    newword = ''
    wordlen = len(word)
    for i in range(wordlen):
        if (newhand.get(word[i].lower(), 0) > 0):                        # we check if the letter is in the hand
            newhand[word[i].lower()] -= 1
            newword += word[i].lower()
        elif((newhand.get('*', 0) > 0) and (word[i].lower() in VOWELS)): # we check if a wildcard can be used
            newhand['*'] -= 1
            newword += '*'
        else:                                                            # if neither then its not in the hand
            inHand = False
            break

    word_equals_word_from_hand = word.lower() == newword                 # we check if the word given is the same as the one we checked for
                                                                         # this is to check for wildcard use

    return (inHand and inList and word_equals_word_from_hand)            # only if all 3 are true do we say the word is valid

    #pass  # TO DO... Remove this line when you implement this function


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """
    Returns the length (number of letters) in the current hand.

    hand: dictionary (string-> int)
    returns: integer
    """
    length = 0
    for i in hand:
        length += hand[i]            #checks number of letters in hand
    return length
    #pass  # TO DO... Remove this line when you implement this function


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand

    """


    score = 0
    while (calculate_handlen(hand) > 0):    # while there are still letters in the hand you can continue to play it
        print("current hand: ",end="")
        display_hand(hand)
        user_input = input('Enter word, or "!!" to indicate that you are finished:')
        if(user_input == '!!'):             # or if you type '!!' to end early
            break
        else:
            if(is_valid_word(user_input,hand,word_list)):     # if the word user inputs is valid then it updates hand and adds points
                newwordscore = get_word_score(user_input,calculate_handlen(hand))
                score += newwordscore
                print("'",user_input,"'"," earned ", newwordscore," points.",end=" ")
                print("Total: ", score," points")
            else:
                print("word is not valid")
        hand = update_hand(hand,user_input)        # if its not valid then as penalty the letters you did have for that word are taken away
    #print("Total: ", score, " points")
    return score                           # returns score of the whole hand

#
# Problem #6: Playing a game
#


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    numletters = hand.get(letter, 0)               # checks how many letters we have for the one we're replacing
    newletter = random.choice(VOWELS+CONSONANTS)    #picks random letter
    while(newletter in hand):
        newletter = random.choice(VOWELS + CONSONANTS)  # makes sure its not one we already have
    if (hand.get(letter, 0)) > 0:                       # puts letter(s) in hand
        hand[letter] = 0
    hand[newletter] = numletters
    return hand

    #pass  # TO DO... Remove this line when you implement this function


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the
      entire series

    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep
      the better of the two scores for that hand.  This can only be done once
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.

    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    numHands = int(input("input a total number of hands")) # inputs number of hands
    entireScore = 0
    changeHandsChances = 1     # number of chances to change hands
    replayHandChances = 1      # number of chances to replay a hand

    for i in range(numHands):
        hand = deal_hand(HAND_SIZE)     #gives a hand
        print("current hand: ",end="")
        display_hand(hand)
        if changeHandsChances > 0:       # gives us an option to change letter. Can do it in the beginnning while we have chances left
            answer = input("Do you wish to substitute one letter for another? If so type 'yes'. This can only be done once per game")
            if answer == "yes":
                newletter = input("Type the letter you wish to replace")
                substitute_hand(hand,newletter)
                changeHandsChances -= 1
        hand_score = play_hand(hand,word_list)    # plays the hand
        if replayHandChances > 0:                 # gives us the option to replay hand while we still have chances left
            answer = input("would you like to replay your hand? If so type 'yes'. This can only be done once per game")
            if answer == "yes":
                hand_score = play_hand(hand, word_list)
                replayHandChances -= 1
        entireScore += hand_score                  # adds score of the hand
        print("Total score for this hand: ", hand_score)
    print("Total score over all hands: ", entireScore)     # prints the total score


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
