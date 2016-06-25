from __future__ import division
__author__ = 'ASM Pushon'

"""
Hangman game in Python. Works in both python 2 and python 3.
Usage: <python hang_man.py>
"""
import time
import random
import getpass
import string
from math import sqrt

from six.moves import input

words = "python awesome programming language love pronunciation life enjoy grammar pragmatic deride pasta salad orange\
            always meaningful creativity sapiens adventure music travel food tennis reading science soup noodle mango\
            technology computer physics cosmology mathematics family friend relation happiness wisdom taco burger banana\
            empathy gratitude dedication joy kindness patience openness commitment curiosity caring cofee sandwich litchi\
            equanimity hopefulness generosity truthfulness serenity respect insight vision sex chocolate cake apple grape\
            determination sympathy smart prudent honesty adorable philanthropist pizza noble altruist tea pineapple".split()
words = tuple(words) # to make it immutable and more memory efficient

graphic0 = """  
________    
|      |      
|             
|             
|             
|
=========
"""     
graphic1 = """
________      
|      |      
|      0       
|             
|             
|
=========
"""  
graphic2 = """
________      
|      |      
|      0       
|     /        
|             
|
=========
"""  
graphic3 = """
________      
|      |      
|      0       
|     / \      
|             
|
=========
"""  
graphic4 = """
________      
|      |      
|      0       
|     /|\       
|            
|
=========
"""  
graphic5 = """
________      
|      |      
|      0       
|     /|\       
|      |      
|
=========
"""
graphic6 = """
________      
|      |      
|      0       
|     /|\       
|      |      
|     /
|
=========
"""  
graphic7 = """
________      
|      |      
|      0       
|     /|\       
|      |      
|     / \\
|
=========   
"""  

hang_graphics = (graphic0, graphic1, graphic2, graphic3, graphic4, graphic5, graphic6, graphic7)

#game settings
#__________________________________________________________________________________________
def initiate_game():
    '''Takes player(s) name(s), game mode, and word as input to initiate each game and return the score(s) in a list'''
    if num_game == 1: #take input for the game mode and player(s) name only at the first game
        intro_msg = '''
Welcome to hangman(/woman) game! Here you have to guess the right word given by the computer\
 or your partner. You will guess a single character at a time. You will have 7 chances to guess\
 the right word. If you fail, you will be hanged to death. Wish you a thrilling time!
        '''
        print(intro_msg)
        time.sleep(2)

        global player1_name
        player1_name = input("Please enter your name ->") or 'Harry'
        player1_name = player1_name[0].upper() + player1_name[1:]   #make the first letter uppercase
        print("Let's start the fun! :)")
        print("Please select the game mode - single or dual mode?")
        print("In single mode you will play with the computer")
        time.sleep(2)
        print("While in dual mode, you will play with another player who will provide the guessing word")
        global game_mode
        game_mode = ''
        while not((game_mode == '1') or (game_mode == '2')):
                   game_mode = input("Enter '1' for single mode and '2' for dual mode ->")
        
        if (game_mode == '2'):
            global player2_name
            player2_name = input("%s, please enter your opponent's name ->" % (player1_name)) or 'Hermaione'
            player2_name = player2_name[0].upper() + player2_name[1:]   #make the first letter uppercase

    # else:
    #     pass #keep the previously selected game mode

    game_points = []
    if (game_mode == '1'):
        random_word = random.choice(words)
        point_scored = inside_game_logic(random_word, player1_name)
        game_points.append(point_scored)

    elif (game_mode == '2'):
        
        def run_game(player1, player2): # player2 will type the word for player1
            '''Takes the provided word as a hidden input, validates it, and uses it to calculate and store the points earned by each player.'''
            word = getpass.getpass("%s, please enter the word for %s (copy/paste allowed) ->" % (player2, player1))
            while ((len(word) < 2) or (len(word) > 29) or not(word.isalpha())):
                word = getpass.getpass("%s, please enter a valid word consists of 2-29 characters ->" % (player2))
            word = word.lower()
            point_scored = inside_game_logic(word, player1)
           
            while(point_scored == -1): # if the word is grammatically incorrect
                print("Sorry %s, as you provided an incorrect word in the the last game, you have to provide a word again." % (player2))
                word = getpass.getpass("%s, please enter the word for %s (copy/paste allowed) ->" % (player2, player1))
                point_scored = inside_game_logic(word, player1)

            game_points.append(point_scored)   

        print("%s, you are gonna guess the word now!" % (player1_name))    
        time.sleep(1)
        run_game(player1_name, player2_name)

        print("Now it's %s's turn." % (player2_name))
        time.sleep(1)
        run_game(player2_name, player1_name)
        
    return game_points

def inside_game_logic(word, player_name):
    '''Take the guessed chracters as input, compare them with the provided word, caculate points, display game
    status, and give proper reward to the player according to the game's logic'''
    num_right_guess = 0
    num_wrong_guess = 0
    point_scored = 0.0
    is_winner = False
    all_guess_chars = []
    num_right_guess_streak = 0
    max_right_guess_streak = 0
    char_index_dict = {char: [ch_ind for ch_ind, ch in enumerate(word) if ch == char] for char in word} #dictionary of unique chars and their indexes  
    
    display_word = '_' * len(word)
    print("Initial state: %s" % ("|".join(display_word)))
    print("%s, you are here: " % (player_name))
    print(graphic0)

    while num_wrong_guess < 7:

        guess_char = input("Guess a character/letter ->")
        guess_char = guess_char.lower()
        all_guess_chars.append(guess_char)
        
        if ((guess_char == None) or (len(guess_char) != 1) or not(guess_char.isalpha())):
            print('Please insert a single alphabetic character at a time')
            all_guess_chars.remove(guess_char)

        elif guess_char in char_index_dict: #if the guess is right
            num_right_guess += 1
            num_right_guess_streak += 1
            if num_right_guess_streak > max_right_guess_streak:
                max_right_guess_streak = num_right_guess_streak #caculate maximum num_guess in a row

            list_guess_char_index = char_index_dict[guess_char]
            if len(list_guess_char_index) == 1: #if guess_char occurs once
                ind = list_guess_char_index[0]
                del char_index_dict[guess_char] #remove the index of guessed char

            elif len(list_guess_char_index) > 1: #else:
                ind = random.choice(list_guess_char_index) #randomly select the position of any repeated char
                char_index_dict[guess_char].remove(ind)

            display_word = display_word[:ind] + guess_char + display_word[ind + 1:]         

            print('\nGood job, %s!' % (player_name))
            print('Current state: %s' % ("|".join(display_word)))
            print('%.2f' % (num_right_guess * 100.0 / len(word)) + ('% of the word completed!'))
                    
            if (num_right_guess == len(word)):  #condition for successfully completing the game
                is_winner = True
                point_scored = (sqrt(2) * num_right_guess) + 7 + 1.3 + 3 + 7 - (2 * num_wrong_guess) #have some personal weakness for #1, 3, 7 :)

                if num_wrong_guess == 0:
                    point_scored += 5
                    print("\nUnbelievable %s, you guessed the whole word without losing any chances!!" % (player_name))
                    print("You got 5 bonus points for making the perfect guess!")
                elif num_wrong_guess == 1:
                    point_scored += 3
                    print("\nIncredible %s, you guessed the whole word by losing just 1 chance!" % (player_name))
                    print("You got 3 bonus points for making that awesome guess!")
                elif num_wrong_guess == 2:
                    point_scored += 2
                    print("\nWow %s, you guessed the whole word by losing only 2 chances!" % (player_name))
                    print("You got 2 bonus points for making that solid guess!")
                else:    
                    print("Awesome, %s! You guessed the whole word correctly!!" % (player_name))
                
                if max_right_guess_streak >= 3:
                    streak_bonus = 0.5 * max_right_guess_streak
                    point_scored += streak_bonus
                    print("Since you guessed %d characters correctly in a row, %.2f bonus points to you!" % (max_right_guess_streak, streak_bonus))

                time.sleep(1)
                print("\nYou're still alive!! Now have some fun and smile for a bit. :)")
                print("%s earned %.2f points in this game" % (player_name, point_scored))
                break
        
        elif not(guess_char in char_index_dict): #Guessed the wrong character
            num_wrong_guess += 1
            num_right_guess_streak = 0
            print("\nOops, not the right guess.. :(  Try again please.")
            print("Current state: %s" % ("|".join(display_word)))
            print("Chance(s) remaining: %d more chances" % (7 - num_wrong_guess))
            print("Characters guessed so far: %r" % (all_guess_chars))
            time.sleep(1)
            if num_wrong_guess == 1:
                print("%s, your hanging process just started dear, be careful..." % (player_name))
            elif num_wrong_guess == 4:
                print("%s, you are getting closer to be hanged dear, try little harder..." % (player_name))
            elif num_wrong_guess == 6:
                print("%s, you are just one mistake away from being hanged dear, give your best effort.." % (player_name))
            print("%s, at this moment you are here: " % (player_name))
            print(hang_graphics[num_wrong_guess])
       
    if not(is_winner):

        def final_message():
            '''Show message to current player is he/she failed to guess the correct word'''
            if (num_right_guess * 100.0 / len(word)) > 70:
                point_scored = sqrt(3 * len(word)) * (num_right_guess * 1.0 / len(word))
                print("Since %s guessed more than 70 percent of the word correctly, he/she scored a bit." % (player_name))
                print("%s earned %.2f points in this game" % (player_name, point_scored))

                print("Game over! You will be hanged now!")
                print("What's your last wish, Mr/Ms %s? What are the memories you remember at this moment??" % (player_name))

        if (game_mode == '2'):
            print("The right word was: %s" % (word))
            time.sleep(1)

            print("Now %s and %s, do you agree that '%s' is a valid word in english language?" % (player1_name, player2_name, word))
            players_consent = input("Enter 'n' or 'no' if you do not(default value is 'yes') >")
            if (players_consent.lower().startswith('n')): # if players agree that the given word is not a valid word
                point_scored = -1
            else:
                final_message()

        else:   #game_mode == '1'
            final_message()

    return point_scored


if __name__ == '__main__':
    
    num_game = 0
    play_continue = True
    all_points = []

    while play_continue:
        num_game += 1
        game_points = initiate_game()
        all_points += game_points

        print("\nDo you want to continue playing/hanging?")
        user_consent = input("Enter 'y' to continue or 'n' to exit the game. ->")

        if (user_consent.lower().startswith('n')):
            play_continue = False
            if (game_mode == '1'):
                total_point = sum(all_points)
                num_game_won = len([point for point in all_points if point > 9.07])
                print("\nFinal statistics:")
                print("%s, you won %d games out of %d games" % (player1_name, num_game_won, num_game))
                time.sleep(1)
                print("Your total score is %.2f points in %d games" % (total_point, num_game))
                print("Your average score is %.3f points per game" % (1.0 * total_point / num_game))
                print("Thanks for playing! I hope you enjoyed it. Have fun!")

            else:   #game_mode == '2'
                player1_points = all_points[0::2]
                player1_total_point = sum(player1_points)
                player1_num_game_won = len([point for point in player1_points if point > 9.07])
                player2_points = all_points[1::2]
                player2_total_point = sum(player2_points)
                player2_num_game_won = len([point for point in player2_points if point > 9.07])

                print("\nFinal statistics:")
                print("%s won %d games out of %d games" % (player1_name, player1_num_game_won, num_game))
                print("%s won %d games out of %d games" % (player2_name, player2_num_game_won, num_game))
                time.sleep(1)
                print("%s's total score is %.2f points in %d games" % (player1_name, player1_total_point, num_game))
                print("%s's total score is %.2f points in %d games" % (player2_name, player2_total_point, num_game))
                time.sleep(1)
                print("%s's average score is %.3f points per game" % (player1_name, (1.0 * player1_total_point / num_game)))
                print("%s's average score is %.3f points per game" % (player2_name, (1.0 * player2_total_point / num_game)))
                time.sleep(1)
                
                if (player1_total_point > player2_total_point):
                    print("Therefore, %s is the winner! Congratulations %s. :)" % (player1_name, player1_name))
                    print("%s, don't be upset.. try again, you will win. Finger crossed!" % (player2_name))
                elif (player2_total_point > player1_total_point):
                    print("Therefore, %s is the winner! Congratulations %s. :)" % (player2_name, player2_name))
                    print("%s, don't be upset.. try again, you will win. Finger crossed!" % (player1_name))
                else:
                    print("Both of you are the winner! :)")
                
                time.sleep(1)
                print("%s and %s, thanks for playing! I hope both of you enjoyed it. Have a nice day!" % (player1_name, player2_name))
