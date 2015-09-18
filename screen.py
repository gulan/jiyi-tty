#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import curses

"""
start_game
display ?
user_prod
start_dialog
"""

TOSS,KEEP = 'TOSS','KEEP'

class screen:

    def display_question(self,lines):
        self.stdscr.clear()
        i = 0
        while i < len(lines):
            self.stdscr.addstr(i,0,lines[i])
            i += 1
        self.next_pos = i
        self.stdscr.refresh()
        
    def user_prod(self):
        while 1:
            ch = self.stdscr.getch()
            if ch == 10:
                break

    def display_answer(self,lines):
        i = self.next_pos
        while i < len(lines) + self.next_pos:
            self.stdscr.addstr(i,0,lines[i-self.next_pos])
            i += 1
        self.stdscr.refresh()
        
    def user_score(self):
        while 1:
            ch = self.stdscr.getch()
            if ch in (10,curses.KEY_DC):
                break
        return (TOSS if ch == curses.KEY_DC else KEEP)
        
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)

    def cleanup(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
