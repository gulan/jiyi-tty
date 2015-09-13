#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import curses

class screen:

    def question(self,lines):
        self.stdscr.clear()
        i = 0
        while i < len(lines):
            self.stdscr.addstr(i,0,lines[i])
            i += 1
        self.next_pos = i
        self.stdscr.refresh()
        while 1:
            ch = self.stdscr.getch()
            if ch == 10:
                break

    def answer(self,lines):
        i = self.next_pos
        while i < len(lines) + self.next_pos:
            self.stdscr.addstr(i,0,lines[i-self.next_pos])
            i += 1
        self.stdscr.refresh()
        while 1:
            ch = self.stdscr.getch()
            if ch in (10,curses.KEY_DC):
                break
        return ch == curses.KEY_DC

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
