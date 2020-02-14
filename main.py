#!/usr/bin/env python3

# Moved main() from chinese.py, as that module should not know about
# the dialog and screen modules.

# Should the database have a cleanup()?

import screen
import chinese
import dialog

def main(count=12):
    gs = chinese.SQL(count)
    sc = screen.new_screen()
    dialog.loop(gs,sc)
    sc.cleanup()

main()

