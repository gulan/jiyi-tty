#!/usr/bin/env python3

# moved main() from chinese.py, as that module should not know about
# the dialog and screen modules.

# should the data base have a cleanup()?

import screen
import chinese
import dialog

def main(count=20):
    log = open('dialog.log', 'a')
    gs = chinese.SQL(count)
    sc = screen.new_screen(log)
    dialog.loop(gs,sc,log)
    sc.cleanup()
    log.close()

main()

