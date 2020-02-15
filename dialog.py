#!/usr/bin/env python3

from screen import TOSS

VERSION = '4.0.0'

FLIPA     = '0-user-prod-a'
FLIPB     = '0-user-prod-b'
SCORE     = '0-user-score'
ITER      = '1-iter-again'
ITER_END  = '1-iter-end'
EXIT      = 'EXIT'

def loop(db,device):
    state = ITER
    while state != EXIT:
        
        if state == ITER_END:
            db.restack()
            state = EXIT if db.gameover else ITER
            continue
            
        if state == ITER:
            device.display_question(db.question,db.progress)
            state = FLIPA
            continue
        
        if state == FLIPA:
            device.accept_flip()
            state = FLIPB
            continue
        
        if state == FLIPB:
            device.display_answer(db.answer,db.progress)
            state = SCORE
            continue
        
        if state == SCORE:
            db.toss() if device.accept_score() == TOSS else db.keep()
            state = ITER if db.more else ITER_END
            continue

