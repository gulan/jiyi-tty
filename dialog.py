#!/usr/bin/env python3

import chinese
import screen

VERSION = '4.0.0'

def loop(gs,sc):
    state = '1-iter-again'
    while state != 'EXIT':

        if state == '1-iter-end':
            gs.restack()
            state =  '0-iter-end' if gs.gameover else '1-iter-again'
            continue
            
        if state == '1-iter-again':
            sc.display_question(gs.question)
            state = '0-user-prod'
            continue
        
        if state == '0-user-prod':
            sc.user_prod()
            sc.display_answer(gs.answer)
            state = '0-user-score'
            continue
        
        if state == '0-user-score':
            if sc.user_score() == screen.TOSS:
                gs.toss()
            else:
                gs.keep()
            state = '1-iter-again' if gs.more else '1-iter-end'
            continue
            
        if state == '0-iter-end':
            gs.check_endgame()
            state = 'EXIT'
            continue

def dialog():
    "Run game with a screen server process."
    gs = chinese.SQL(10)
    try:
        sc = screen.screen_xmlrpc()
        loop(gs,sc)
    finally:
        sc.cleanup()

def dialog_local():
    "Run game as a regular program, no IPC. See play.py"
    gs = chinese.SQL(10)
    sc = screen.screen()
    loop(gs,sc)
    sc.cleanup()

if __name__ == '__main__':
    dialog_local()
