#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

# Class screen was orignally made to be imported into a standalone
# game. The xmlrpc wrapper was added later.

# It might seen strange that talking to a screen means going though a
# server, but this setup is common. We own one centralized database,
# but there could be many remote players.

# As an xml server, the module must be running before the user tries
# running the game (dialog.py).

# ansi_flashcard does not yet have a simple launcher that will start
# the screen server only if needed, before starting the dialog
# process. This might be convenient now, but is of no use for a
# distributed system, where the server must always be runnung.

import curses
import sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client

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

def run_screen_server(addr):
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)
    server = SimpleXMLRPCServer(
        addr,
        requestHandler=RequestHandler,
        logRequests=False,
        allow_none=True)
    server.register_instance(screen())
    server.serve_forever()
    sys.exit()

def screen_xmlrpc(addr=("localhost",8005)):
    return xmlrpc.client.ServerProxy('http://%s:%s' % addr)

def play_actions(c):
    # a test.
    c.display_question(['Hello',' world'])
    c.user_prod()
    c.display_question(['Yes'])
    c.user_score()
    

if __name__ == '__main__':
    run_screen_server(("localhost",8005))
