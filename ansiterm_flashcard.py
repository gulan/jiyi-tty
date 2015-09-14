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

VERSION = '3.0.1'
ENTER,DELETE = 10,127

class State:
    def __init__(self):
        self.state = None

def loop0(gs,sc,w):
    w.state = '0-iter-end' if gs.gameover else '0-iter-again'
    while w.state != '0-exit-loop':

        if w.state == '0-iter-again':
            w.state = '1-iter-again'
            continue
            
        if w.state == '1-iter-end':
            gs.restack()
            w.state = '0-iter-end' if gs.gameover else '0-iter-again'
            continue
            
        if w.state == '1-iter-again':
            sc.question(gs.question)
            if sc.answer(gs.answer):
                gs.toss()
            else:
                gs.keep()
            w.state = '1-iter-again' if gs.more else '1-iter-end'
            continue
            
        if w.state == '1-iter-end':
            w.state = '1-exit-loop'
            continue

        if w.state == '0-iter-end':
            gs.check_endgame()
            w.state = '0-exit-loop'
            continue

def dialog():
    w = State()
    gs = chinese.chinese_list(10)
    try:
        sc = screen.screen()
        loop0(gs,sc,w)
    finally:
        sc.cleanup()


if __name__ == '__main__':
    dialog()
    
