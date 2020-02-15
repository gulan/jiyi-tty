#!/usr/bin/env python3

import screen

VERSION = '4.0.0'

FLIPA     = '0-user-prod-a'
FLIPB     = '0-user-prod-b'
SCORE     = '0-user-score'
ITER      = '1-iter-again'
ITER_END0 = '0-iter-end'
ITER_END1 = '1-iter-end'
EXIT      = 'EXIT'

def loop(database,device):
    state = ITER
    while state != EXIT:
        
        if state == ITER_END1:
            database.restack()
            state =  ITER_END0 if database.gameover else ITER
            continue
            
        if state == ITER:
            tossed = database.progress()
            device.display_question(database.question,tossed)
            state = FLIPA
            continue
        
        if state == FLIPA:
            device.accept_flip()
            state = FLIPB
            continue
        
        if state == FLIPB:
            tossed = database.progress()
            device.display_answer(database.answer,tossed)
            state = SCORE
            continue
        
        if state == SCORE:
            if device.accept_score() == screen.TOSS:
                database.toss()
            else:
                database.keep()
            state = ITER if database.more else ITER_END1
            continue
            
        if state == ITER_END0:
            database.check_endgame()
            state = EXIT
            continue

