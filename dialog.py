#!/usr/bin/env python3

import chinese
import screen

VERSION = '4.0.0'

class State:
    def __init__(self):
        self.state = None

def loop0(gs,sc,w):
    w.state = '0-iter-end' if gs.gameover else '1-iter-again'
    while w.state != 'EXIT':

        if w.state == '1-iter-end':
            gs.restack()
            w.state =  '0-iter-end' if gs.gameover else '1-iter-again'
            continue
            
        if w.state == '1-iter-again':
            sc.display_question(gs.question)
            w.state = '0-user-prod'
            continue
        
        if w.state == '0-user-prod':
            sc.user_prod()
            sc.display_answer(gs.answer)
            w.state = '0-user-score'
            continue
        
        if w.state == '0-user-score':
            if sc.user_score() == screen.TOSS:
                gs.toss()
            else:
                gs.keep()
            w.state = '1-iter-again' if gs.more else '1-iter-end'
            continue
            
        if w.state == '0-iter-end':
            gs.check_endgame()
            w.state = 'EXIT'
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
