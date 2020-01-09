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

# xmlrpc allows me to convert an object into a proxy to a server. The
# original object is in the server. The proxy implelemts the objects
# methods, but turns them into message that are sent to the
# server. the goal is to transparently replace the object in an
# application with the proxy.

# of course, the create method for the object and server will differ,
# but once created, they act the same. what about destruction? does
# the end of the game also destroy the server? do the server need to
# add to the interface of screen?

import curses
import os
import sys
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

TOSS,KEEP = 'TOSS','KEEP'
ENTER = 10
DELETE = curses.KEY_DC

class screen:

    def display_question(self,lines):
        for w in lines:
            self.log.write(w + "\n")
        self.stdscr.clear()
        i = 0
        while i < len(lines):
            self.stdscr.addstr(i,0,lines[i])
            i += 1
        self.next_pos = i
        self.stdscr.refresh()
        
    def user_prod(self):
        while self.stdscr.getch() != ENTER:
            pass

    def display_answer(self,lines,toss_count):
        for w in lines:
            self.log.write(w + "\n")
        i = self.next_pos
        while i < len(lines) + self.next_pos:
            self.stdscr.addstr(i,0,lines[i-self.next_pos])
            i += 1
        self.stdscr.addstr(self.nlines-1,self.ncols-6,str(toss_count))
        self.stdscr.refresh()
        
    def user_score(self):
        while 1:
            ch = self.stdscr.getch()
            if ch in (ENTER,DELETE):
                break
        r = (TOSS if ch == DELETE else KEEP)
        self.log.write("S> %s\n" % r)
        return r
                
    def __init__(self, log):
        self.log = log
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        curses.curs_set(0)  # invisible cursor
        (self.ncols,self.nlines) = os.get_terminal_size()

    def cleanup(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

def run_screen_server(addr):

    class RH(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    server = SimpleXMLRPCServer(addr, requestHandler=RH, logRequests=False, allow_none=True)
    server.register_instance(screen())
    server.serve_forever()
    sys.exit()

class app:
    def __init__(self, server, proxy):
        self.server = server
        self.proxy = proxy

    def __getattribute(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            proxy = object.__getattribute__(self, 'proxy')
            return getattr(proxy, name)

    def terminate(self):
        server = object.__getattribute__(self, 'server')
        server.terminate()
        server.join()

def new_screen(log, local=True):
    # Client gets an instance that behaves like a screen, but cannot
    # tell if it is local or remote.
    if local:
        return screen(log)
    else:
        addr = ("localhost", 8005)
        s = multiprocessing.Process(target=run_screen_server, args=(addr,))
        s.start()
        c = xmlrpc.client.ServerProxy('http://%s:%s' % addr)
        return app(s, c)
