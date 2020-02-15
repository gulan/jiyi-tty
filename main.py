#!/usr/bin/env python3

from screen import screen
from chinese import SQL
from dialog import loop

def main(count=12):
    db = SQL(count)
    device = screen()
    loop(db,device)
    device.cleanup()

main()

