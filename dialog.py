#!/usr/bin/env python3

import chinese
import screen

VERSION = '4.0.0'

def loop(gs,sc,log):
    log.write("---- new play ----\n")
    tossed = 0
    state = '1-iter-again'
    while state != 'EXIT':
        
        # log.write("state: %s\n" % state)
        
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
            sc.display_answer(gs.answer,tossed)
            state = '0-user-score'
            continue
        
        if state == '0-user-score':
            if sc.user_score() == screen.TOSS:
                gs.toss()
                tossed += 1
            else:
                gs.keep()
            state = '1-iter-again' if gs.more else '1-iter-end'
            continue
            
        if state == '0-iter-end':
            gs.check_endgame()
            state = 'EXIT'
            continue

# def dialog():
#     "Run game with a screen server process."
#     gs = chinese.SQL(10)
#     try:
#         sc = screen.screen_xmlrpc()
#         loop(gs,sc)
#     finally:
#         sc.cleanup()

def dialog_local():
    "Run game as a regular program, no IPC. See play.py"
    log = open('dialog.log', 'a')
    gs = chinese.SQL(100)
    sc = screen.new_screen(log)
    loop(gs,sc,log)
    sc.cleanup()
    log.close()
