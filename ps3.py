import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}


WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
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
    Given a sequence (string), returns a dictionary with letters as keys and the
    number of times they appear in the sequence as the values.
    e.g.: 'apple' --> ['a':1, 'p':2,'l':1,'e':1]
    """
    
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (The code above is not written by me, it was provided as helper code.)
# -----------------------------------


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

	The score for a word is the product of two components:
	  - The first component is the sum of the points for letters in the word. 
            (points for each letter are the values associated to that letter in the dictionary SCRABBLE_LETTER_VALUES.)
	  - The second component is the larger of: 
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played
    """

    firstcmpnt = 0
    theword = word.lower()
    for letter in theword:
        firstcmpnt += int(SCRABBLE_LETTER_VALUES[letter])
    
    calc = 7*len(theword) - 3*(n-len(theword))
    if calc > 1:
        secondcmpt = calc
    else:
        secondcmpt = 1    

    if len(theword) == 0:
        secondcmpt = 0    

    wordscore = firstcmpnt * secondcmpt
    return int(wordscore)


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1}) --> a x x l l l e
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')     
    print()                              


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    Hand starts with a wildcard '*' that can act as a vowel in a word,
    ceil(n/3)-1 letters in the hand are VOWELS, 
    n - [ceil(n/3)-1] - 1 letters in the hand are CONSONANTS

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.
    """
    
    hand={'*':1}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand


def update_hand(hand, word):
    """
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.
    """
    word = word.lower()
    new_hand = hand.copy()
    for letter in word:
        if letter in new_hand.keys():                   # if the letter is in the keys of the hand dict
            new_hand[letter] = new_hand[letter] - 1     # decrease the int in the corresponding value by 1
            if new_hand[letter] == 0:                   # if the value attached to that letter in the hand dict is 0
                del new_hand[letter]                    # delete the dict entry
    
    return new_hand


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    """
    word = word.lower()
    wild_words = []
    wild = 0
    goodwild = 0
    otherletter = 0 
    overused = 0
    new_hand = hand.copy()

    for letter in word:
        if letter in new_hand.keys():                                            # if letter is present in hand
            new_hand[letter] = new_hand[letter] - 1                              # value attached to that letter is decreased by 1

            if letter == '*':                                                    # if a wildcard is used (denoted by *)
                wild = 1                                                         # assign 1 to wild, representing usage of wildcard
                wild_index = word.find("*")
                for vowel in VOWELS:
                    wild_word = word[:wild_index] + vowel + word[wild_index+1:]  
                    wild_words.append(wild_word)                                 # replace the * with each of the 5 vowels in VOWELS, append the 5 resulted words in wild_words

        else:
            otherletter = -1                                                     # if the letter is not in the hand, assign -1 to otherletter
        
    for freq in new_hand.values():
        if freq < 0:                                                             # if the value attached to any letter in the hand dict is negative, this means it has been overused 
            overused = -1                                                        # assign -1 to overused

    if wild == 1:          
        for word in wild_words:
            if word in word_list:                                                # if any word in the wild_words list is in word_list
                goodwild = 1                                                     # assign 1 to goodwild

    if word in word_list: 
        if otherletter == 0 and overused == 0:                                   
            return True                                                          # return True if word is in wordlist and all letters of the word are present in hand and no letters have been overused
    elif wild == 1:
        if goodwild == 1 and otherletter == 0 and overused == 0:
            return True                                                          # return True if wildcard has been used and the wild word is present in word_list, and all letters of the word are in hand and none have been overused
    else:
        return False


def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    """
    len = 0
    for letter in hand.keys():
        len += int(hand[letter])
    return len


def play_hand(hand, word_list, justsubs):

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

    returns: the total score for the hand
    """

    totalpoints = 0

    while calculate_handlen(hand) > 0:
    
        print("Current hand:", end=' ')
        display_hand(hand)

        user_input = input("Enter word, or '!!' to indicate that you are finished: ")

        if user_input == "!!":
            break

        else:
            if is_valid_word(user_input, hand, word_list):                               # if the word is valid (checked by the function is_valid_word)
                wordpoints = get_word_score(user_input,len(hand))                        # assign the points earned (calculated by get_word_score) to wordpoints
                totalpoints += wordpoints                                               
                print(user_input, "earned", wordpoints, "points. Total:", totalpoints)
            
            else:
                print("That is not a valid word. Please choose another word.")
            
            
            hand = update_hand(hand, user_input)                                         # after each turn, use update_hand to update the hand after removing the letters used in the word


    if calculate_handlen(hand) == 0:
        print("Ran out of letters. Total score:", totalpoints, "points")
    else:
        print("Total score:", totalpoints, "points")
        print("----------")

    return totalpoints    


def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. 

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    """

    thishand = hand.copy()

    entirealpha = "abcdefghijklmnopqrstuvwxyz"

    replacement_letter = random.choice(entirealpha)

    while replacement_letter in thishand.keys():                                            # choose at random from the dict until that letter is not in hand already
        replacement_letter = random.choice(entirealpha)
   
    thishand[replacement_letter] = thishand[letter]                                         # the value associated with the letter (that user wants to replace) also becomes the value associated with the replacement_letter 
    del thishand[letter]                                                                    # delete the entry with the letter user wants to replace

    return thishand


def play_game(word_list):
    """
    Allow the user to play a series of hands
    
    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands
    """
    numhands = int(input("Enter total number of hands: "))
    replay = 0                                                                        # 0 if that hand has not been replaid yet, 1 if the user has already replayed that hand
    subsitution = 0                                                                   # 0 if no substitution of letter has been done in the game yet, 1 if a substitution has already been carried out
    scorelist = []

    for i in range(numhands):
        justsubs = 0                                                                  # justsubs being 1 means a word has just been substituted in this turn, otherwise it's vise versa
        current_hand = deal_hand(HAND_SIZE)
        print("Current hand:", end=' ')
        display_hand(current_hand)

        if subsitution == 0:
            sub_or_not = input("Would you like to substitute a letter? ").lower()     # the option to substitute letter is available if no substitution has taken place before

            if sub_or_not == "yes":
                subsitution = 1                                                       
                justsubs = 1
                userchoiceletter = input("Which letter would you like to replace: ")
                current_hand = substitute_hand(current_hand, userchoiceletter)
        
        firstcurrent = play_hand(current_hand, word_list,justsubs)
        

        if replay == 0:  
            playagain = input("Would you like to replay the hand?: ").lower()
            
            if playagain == "yes":
                replay = 1
                secondcurrent = play_hand(current_hand, word_list, justsubs)
            
                if firstcurrent >= secondcurrent:                                      # keep the higher score of the hand played first time vs after being replayed
                    score1 = firstcurrent
                else:
                    score1 = secondcurrent

            else: 
                score1 = firstcurrent
        
        else:
            score1 = firstcurrent
            
        scorelist.append(score1)
    
    print("----------")
    print("Total score over all hands:", sum(scorelist))
        
            
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
