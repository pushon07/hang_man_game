__author__ = 'ASM Pushon'

"""
Hangman game in Python
Usage: <python hang_man.py>
"""
import time
#import numpy as np
import random

words = "python awesome programming language love pronunciation life enjoy grammar pragmatic deride\
            always meaningful creativity sapiens adventure music travel food tennis reading science\
            technology computer physics cosmology mathematics family friend relation happiness wisdom\
            empathy gratitude dedication joy kindness patience openness commitment curiosity caring\
            equanimity hopefulness generosity truthfulness serenity respect insight vision sex".split()

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
"""  
graphic7 = """
________      
|      |      
|      0       
|     /|\       
|      |      
|     / \
|        
"""  

hang_graphics = [graphic0, graphic1, graphic2, graphic3, graphic4, graphic5, graphic6, graphic7]

#game settings
#__________________________________________________________________________________________
rand_word = random.choice(words)
#rand_word = 'alwaysayhay'
character_remaining = rand_word

num_wrong_guess = 0
display_word = '_' * len(rand_word)

is_winner = False

print "Let's start the fun! :)"
print 'Initial state: %r' % ("|".join(display_word))
print "You are here: ", graphic0

while num_wrong_guess < 7:
    guess_char = raw_input("Guess a character/letter ->")
    
    if len(guess_char) > 1:
        print 'Please insert a single character at a time'

    elif len(guess_char) < 1:
        print 'Please insert a single character'
    
    elif guess_char in character_remaining:
        character_remaining = character_remaining.replace(guess_char, '', 1)
        if not(guess_char in display_word):
            ind = rand_word.index(guess_char)
            display_word = display_word[:ind] + guess_char + display_word[ind + 1:]

        elif guess_char in display_word: #for repeated characters; upto 4 repeatations
            num_repeat_rand = rand_word.count(guess_char)
            num_repeat_display = display_word.count(guess_char)

            if ((num_repeat_rand > 1) and (num_repeat_display == 1)):
                ind_all = [i for i, char in enumerate(rand_word) if char == guess_char]
                display_word = display_word[:ind_all[1]] + guess_char + display_word[ind_all[1] + 1:]

            elif ((num_repeat_rand > 2) and (num_repeat_display == 2)):
                ind_all = [i for i, char in enumerate(rand_word) if char == guess_char]
                display_word = display_word[:ind_all[2]] + guess_char + display_word[ind_all[2] + 1:]

            elif ((num_repeat_rand > 3) and (num_repeat_display == 3)):
                ind_all = [i for i, char in enumerate(rand_word) if char == guess_char]
                display_word = display_word[:ind_all[3]] + guess_char + display_word[ind_all[3] + 1:]
        
        print 'Good job!'
        print 'Current state: %r' % ("|".join(display_word))
        print "%r percent completed!" % (100.0 - len(character_remaining) * 100 / len(rand_word))
                
        if (len(character_remaining) < 1): #condition for successfully completing the game
            is_winner = True
            print "Awesome! You won the game!!"
            print "You're alive!! Now have some fun and smile for bit. :)"
            break
    
    elif not(guess_char in character_remaining): #Guessed the wrong character
        num_wrong_guess += 1
        print "Oops, not the right guess.. :("
        print 'Try again please'
        print 'Current state: %r' % ("|".join(display_word))
        print "Chance(s) remaining: %d more chances" % (7 - num_wrong_guess)
        print hang_graphics[num_wrong_guess]
       
if not(is_winner):        
    print "Game over! You will be hanged now!"
    print "What's your last wish? What are the memories you remember at this moment??"
