To Play
----------------------------------------
> ./main.py

The program will select a few cards from the database, and will
present them one at a time. Press enter to flip a card and reveal the
answer. If you feel that you know the card, press the delete key to
remove from play. Press enter if the card is not yet learned. It will
be presented again (and again) until it is learned. The game ends when
there are no more unlearned cards.

Install
----------------------------------------
For now, I just run ./main.py from the repository directory. Before
that will work, the database needs to be built.

    sqlite3 <hsk2009.sql hsk2009.db

The script runs with Python 3 only. There are no external dependencies,
except that curses must installed on your Linux system.

You might need to fiddle with your terminal configuration to get the
delete key to emit the value that the program expects.

This program makes no use of the network.
