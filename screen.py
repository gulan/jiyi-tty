#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import curses
import os

TOSS, KEEP    = 'TOSS', 'KEEP'
ENTER, DELETE = 10, curses.KEY_DC

class screen:

    def display_question(self,lines,toss_count):
        self.stdscr.clear()
        i = 0
        while i < len(lines):
            self.stdscr.addstr(i,0,lines[i])
            i += 1
        self.next_pos = i
        (ncols,nlines) = os.get_terminal_size()
        self.stdscr.addstr(nlines-1,ncols-6,str(toss_count))
        self.stdscr.refresh()
        
    def accept_flip(self):
        while self.stdscr.getch() != ENTER:
            pass

    def display_answer(self,lines,toss_count):
        i = self.next_pos
        while i < len(lines) + self.next_pos:
            self.stdscr.addstr(i,0,lines[i-self.next_pos])
            i += 1
        (ncols,nlines) = os.get_terminal_size()
        self.stdscr.addstr(nlines-1,ncols-6,str(toss_count))
        self.stdscr.refresh()
        
    def accept_score(self):
        while 1:
            ch = self.stdscr.getch()
            if ch in (ENTER,DELETE):
                break
        r = (TOSS if ch == DELETE else KEEP)
        return r
                
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        curses.curs_set(0)  # invisible cursor

    def cleanup(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
