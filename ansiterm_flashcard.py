#!/usr/bin/env python3

import chinese
# import fcntl
# import os
import random
import screen
import sqlite3
import sys
# import termios

"""
Work though a deck of flashcards. Learned cards are discarded. Missed
cards are saved to a retry deck. When the draw deck is empty, it is
replaced by a shuffled retry deck. The game ends when all the cards
have been learned.

This script is a simplified variant of another flashcard program that
I wrote. Here, the user responses are restricted to just show-card,
save-card and toss-card. In this version the users cannot request that
the deck be restacked nor can they get a progress report. These
restrictions made it simple to code the dialog in block-structured
form, rather than as a state machine.

Version 2 changes 
-----------------
I made the game state a class instance that conforms to an API. The
API can hide the implementation details of how the cards are
represented. For example, the implementation seen here loads cards from
an SQL database into python data structures, and implements the game
operations on those in-memory structures. An alternative
implementation would have all those operations be implemented as SQL
queries on the database.

Beyond insulation from implementation details, the API is abstract
enough that dialog works on any kind of subject deck, as long as the
cards may be seen as having question and answer properties.

The big payoff, though, is that the code for dialog() is clear and
simple.

Version 3 Changes 
-----------------
* Converted to project
* Split out deck and ui stuff to separate modules
* Use curses, which required conversion to python3
"""

VERSION = '3.0.0'
ENTER,DELETE = 10,127

def dialog(gs):
    sc = screen.screen()
    try:
        while not gs.gameover:
            while gs.more:
                sc.question(gs.question)
                if sc.answer(gs.answer):
                    gs.toss()
                else:
                    gs.keep()
            gs.restack()
        gs.check_endgame()
    finally:
        sc.cleanup()

if __name__ == '__main__':
    dialog(chinese.chinese_list(30))
    
