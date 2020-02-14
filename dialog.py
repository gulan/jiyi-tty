#!/usr/bin/env python3

import screen
import time

VERSION = '4.0.0'

FLIPA     = '0-user-prod-a'
FLIPB     = '0-user-prod-b'
SCORE     = '0-user-score'
ITER      = '1-iter-again'
ITER_END0 = '0-iter-end'
ITER_END1 = '1-iter-end'
EXIT      = 'EXIT'

def loop(gs,sc,log):
    log.write("---- new play ----\n")
    start = time.time()
    log.write("T> %s\n" % time.strftime("%Y-%m-%d %H:%M"))
    tossed = 0
    state = ITER
    while state != EXIT:
        
        if state == ITER_END1:
            gs.restack()
            state =  ITER_END0 if gs.gameover else ITER
            continue
            
        if state == ITER:
            sc.display_question(gs.question)
            state = FLIPA
            continue
        
        if state == FLIPA:
            sc.accept_flip()
            state = FLIPB
            continue
        
        if state == FLIPB:
            sc.display_answer(gs.answer,tossed)
            state = SCORE
            continue
        
        if state == SCORE:
            if sc.accept_score() == screen.TOSS:
                gs.toss()
                tossed += 1
            else:
                gs.keep()
            state = ITER if gs.more else ITER_END1
            continue
            
        if state == ITER_END0:
            gs.check_endgame()
            duration = int(time.time() - start)
            log.write("D> %s\n" % duration)
            state = EXIT
            continue

