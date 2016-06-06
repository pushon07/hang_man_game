from __future__ import division
__author__ = 'ASM Pushon'

"""
Hangman game in Python
Usage: <python hang_man.py>
"""
import time
import random
import getpass
from math import sqrt

words = "python awesome programming language love pronunciation life enjoy grammar pragmatic deride pasta salad orange\
            always meaningful creativity sapiens adventure music travel food tennis reading science soup noodle mango\
            technology computer physics cosmology mathematics family friend relation happiness wisdom taco burger banana\
            empathy gratitude dedication joy kindness patience openness commitment curiosity caring cofee sandwich litchi\
            equanimity hopefulness generosity truthfulness serenity respect insight vision sex chocolate cake apple grape\
            determination sympathy smart prudent honesty adorable philanthropist pizza noble altruist tea pineapple".split()
words = tuple(words) # to make it more memory efficient

graphic0 = """  
________    
|      |      
|             
|             
|             
|
"""     
graphic1 = """
________      
|      |      
|      0       
|             
|             
|
"""  
graphic2 = """
________      
|      |      
|      0       
|     /        
|             
|
"""  
graphic3 = """
________      
|      |      
|      0       
|     / \      
|             
|
"""  
graphic4 = """
________      
|      |      
|      0       
|     /|\       
|            
|
"""  
graphic5 = """
________      
|      |      
|      0       
|     /|\       
|      |      
|
"""
graphic6 = """
________      
|      |      
|      0       
|     /|\       
|      |      
|     /
|
"""  
graphic7 = """
________      
|      |      
|      0       
|     /|\       
|      |      
|     / \
|
|   
"""  

hang_graphics = (graphic0, graphic1, graphic2, graphic3, graphic4, graphic5, graphic6, graphic7)

#game settings
#__________________________________________________________________________________________
def initiate_game():

    if num_game == 1: #take input for the game mode and player(s) name only at the first game
        intro_msg = '''
Welcome to hangman(/woman) game! Here you have to guess the righ word given by the computer\
 or your partner. You will guess a single character at a time. You will have 7 chances to guess the\
 right word. If you fail, you will be hanged to death. Wish you a thrilling time!
        '''
        print intro_msg
        time.sleep(3)

        global player1_name
        player1_name = raw_input("Please enter your name ->") or 'Harry'
        print "Let's start the fun! :)"
        print "Please select the game mode - single or dual mode?"
        print "In single mode you will play with the computer"
        time.sleep(2)
        print "While in dual mode, you will play with another player who will provide the guessing word"
        global game_mode
        game_mode = raw_input("Enter '1' for single mode and '2' for dual mode ->")
        
        while not((game_mode == '1') or (game_mode == '2')):
                   game_mode = raw_input("Please insert '1' or '2' here. ->")
        if (game_mode == '2'):
            global player2_name
            player2_name = raw_input("%s, please enter your opponent's name ->" % player1_name) or 'Hermaione'
        
    # else:
    #     pass #keep the previously selected game mode

    game_points = []
    if (game_mode == '1'):
        random_word = random.choice(words)
        point_scored = inside_game_logic(random_word, player1_name)
        game_points.append(point_scored)

    elif (game_mode == '2'):
        print "%s, you are gonna guess the word now!" % player1_name
        time.sleep(2)
        word = get_word(player1_name, player2_name)
        point_scored = inside_game_logic(word, player1_name)
        game_points.append(point_scored)

        print "Now it's %s's turn." % player2_name
        time.sleep(2)
        word = get_word(player2_name, player1_name)
        point_scored = inside_game_logic(word, player2_name)
        game_points.append(point_scored)

    return game_points

def get_word(player1, player2): # player2 will type the word for player1
    '''Takes the provided word as a hidden input, validates it, and saves in the format.'''
    user_word = getpass.getpass("%s, please enter the word for %s (copy/paste allowed) ->" % (player2, player1))
    while not((len(user_word) > 1) and (len(user_word) < 30)):
        user_word = getpass.getpass("%s, please enter a word consists of 2-29 characters ->" % (player2))
    user_word = user_word.lower()
    return user_word

def disp_word(disp_word_before, word, guess_char, replace_index):
    '''Display the correctly guessed character at their proper position when there is any repeated character.'''
    ind_all = [i for i, char in enumerate(word) if char == guess_char] # all indexes of the repeated char in word
    display_word_after = disp_word_before[:ind_all[replace_index]] + guess_char + disp_word_before[ind_all[replace_index] + 1:]
    return display_word_after

def inside_game_logic(word, player_name):
    character_remaining = word
    num_wrong_guess = 0
    point_scored = 0.0
    display_word = '_' * len(word)
    is_winner = False
    all_guess_chars = []
        
    print 'Initial state: %s' % ("|".join(display_word))
    print "%s, you are here: " % player_name
    print graphic0

    while num_wrong_guess < 7:

        guess_char = raw_input("Guess a character/letter ->")
        all_guess_chars.append(guess_char)
        
        if len(guess_char) > 1:
            print 'Please insert a single character at a time'
            all_guess_chars.remove(guess_char)

        elif len(guess_char) < 1:
            print 'Please insert a single character'
            all_guess_chars.remove(guess_char)

        elif guess_char in character_remaining:
            character_remaining = character_remaining.replace(guess_char, '', 1)
            if not(guess_char in display_word):
                ind = word.index(guess_char)
                display_word = display_word[:ind] + guess_char + display_word[ind + 1:]

            elif guess_char in display_word: #for repeated characters;
                num_occur = word.count(guess_char) #minimum val of num_repeat is 2
                num_occur_display = display_word.count(guess_char)
                num_repeat_allowed = 7

                for num_repeat in xrange(1, num_repeat_allowed+1):
                    if ((num_occur > num_repeat) and (num_occur_display == num_repeat)):
                        display_word = disp_word(display_word, word, guess_char, num_repeat)
                        break

            print 'Good job, %s!' % player_name
            print 'Current state: %s' % ("|".join(display_word))
            print '%.2f' % (100.0 - len(character_remaining) * 100 / len(word)) + '% of the word completed!'
                    
            if (len(character_remaining) < 1): #condition for successfully completing the game
                is_winner = True
                point_scored = (sqrt(2) * len(word)) + 7 + 1.3 + 3 + 7 - (2 * num_wrong_guess) #have some personal weakness for #1, 3, 7 :)

                if num_wrong_guess == 0:
                    point_scored += 5
                    print "Unbelievable %s, you guessed the whole word without losing any chances!!" % (player_name)
                    print "You got 5 bonus points for making the perfect guess!"
                elif num_wrong_guess == 1:
                    point_scored += 3
                    print "Incredible %s, you guessed the whole word by losing just 1 chance!" % (player_name)
                    print "You got 3 bonus points for making that awesome guess!"
                elif num_wrong_guess == 2:
                    point_scored += 2
                    print "Wow %s, you guessed the whole word by losing only 2 chances!" % (player_name)
                    print "You got 2 bonus points for making that solid guess!"
                else:    
                    print "Awesome, %s! You guessed the whole word correctly!!!!" % (player_name)
                
                print "You're still alive!! Now have some fun and smile for bit. :)"
                print "%s earned %.2f points in this game" % (player_name, point_scored)
                break
        
        elif not(guess_char in character_remaining): #Guessed the wrong character
            num_wrong_guess += 1
            print "Oops, not the right guess.. :("
            print 'Try again please'
            print 'Current state: %s' % ("|".join(display_word))
            print "Chance(s) remaining: %d more chances" % (7 - num_wrong_guess)
            print "Characters guessed so far: %r" % all_guess_chars
            print hang_graphics[num_wrong_guess]
       
    if not(is_winner):
        if (game_mode == '2'):
            print "The right word was: %s" % word
            time.sleep(1)

        if (len(character_remaining) * 100.0 / len(word)) < 30:
            point_scored = sqrt(3 * len(word)) * (1 - (len(character_remaining) * 1.0 / len(word)))
            print "Since %s guessed more than 70 percent of the word correctly, he/she scored a bit." % player_name
            print "%s earned %.2f points in this game" % (player_name, point_scored)

        print "Game over! You will be hanged now!"
        print "What's your last wish, %s? What are the memories you remember at this moment??" % player_name
        
    return point_scored


if __name__ == '__main__':
    
    num_game = 0
    play_continue = True
    all_points = []

    while play_continue:
        num_game += 1
        game_points = initiate_game()
        all_points += game_points

        print "Do you want to continue playing/hanging?"
        user_consent = raw_input("Enter 'y' to continue and 'n' to exit the game. ->") or 'y'
        user_consent = user_consent.lower()

        while not((user_consent == 'y') or (user_consent == 'n')):
               user_consent = raw_input("Please insert 'y' or 'n' here. ->")

        if user_consent == 'n':
            play_continue = False
            if (game_mode == '1'):
                total_point = sum(all_points)
                num_game_won = len([point for point in all_points if point > 9.07])
                print "Final statistics:"
                print "%s, you won %d games out of %d games" % (player1_name, num_game_won, num_game)
                time.sleep(1)
                print "Your total score is %.2f points in %d games" % (total_point, num_game)
                print "Your average score is %.3f points per game" % (1.0 * total_point / num_game)
                print "Thanks for playing! I hope you enjoyed it. Have fun!"

            else:   #game_mode == '2'
                player1_points = all_points[0::2]
                player1_total_point = sum(player1_points)
                player1_num_game_won = len([point for point in player1_points if point > 9.07])
                player2_points = all_points[1::2]
                player2_total_point = sum(player2_points)
                player2_num_game_won = len([point for point in player2_points if point > 9.07])

                print "Final statistics:"
                print "%s won %d games out of %d games" % (player1_name, player1_num_game_won, num_game)
                print "%s won %d games out of %d games" % (player2_name, player2_num_game_won, num_game)
                time.sleep(1)
                print "%s's total score is %.2f points in %d games" % (player1_name, player1_total_point, num_game)
                print "%s's total score is %.2f points in %d games" % (player2_name, player2_total_point, num_game)
                time.sleep(1)
                print "%s's average score is %.3f points per game" % (player1_name, (1.0 * player1_total_point / num_game))
                print "%s's average score is %.3f points per game" % (player2_name, (1.0 * player2_total_point / num_game))
                time.sleep(1)
                
                if (player1_total_point > player2_total_point):
                    print "Therefore, %s is the winner! Congratulations %s. :)" % (player1_name, player1_name)
                    print "%s, don't be upset.. try again, you will win. Finger crossed!" % (player2_name)
                elif (player2_total_point > player1_total_point):
                    print "Therefore, %s is the winner! Congratulations %s. :)" % (player2_name, player2_name)
                    print "%s, don't be upset.. try again, you will win. Finger crossed!" % (player1_name)
                else:
                    print "Both of you are the winner! :)"
                
                time.sleep(1)
                print "%s and %s, thanks for playing! I hope both of you enjoyed it. Have a nice day!" % (player1_name, player2_name)