Version 4
----------------------------------------
My goal is to allow program to suspend while awaiting user input. I do
not want keep the states of thousands of users in active processes. I
have to save the session state in some ecomonical form, and then use
it to restart the game at the proper place. The are two possible
locations for the state store: in my database or hidden within the
client's display. (Amusingly, this choice was already known in the 1970's)

I will try using the database.

My screen is defined by a running curses process. This process must
remain running during the entire course of the user's game, otherwise
there would be nothing listening for the user's input. The dialog
state machine may be restarted, however.

  * make the screen a distinct process. 
  * screen starts a new instance of the dialog machine upon user's input.

Assume that a user is remote and has a dedicated tty and a dialog
process attached to it. These resources persist at least as long as a
single game.

The dialog is a

  * Separate process for each user dialog need not continue running
    while waiting for user input

  * There should be a dispatching server that accept user's responses
    and starts a dialog process.

  * On a single computer implementation, the user process could spawn
    a dialog as needed, but the remote-clients / local-server design
    is more general.

Version 3
----------------------------------------
* Converted to project
* Split out deck and ui stuff to separate modules
* Use curses, which required conversion to python3

Version 2
----------------------------------------
I made the game state a class instance that conforms to an API. The
API can hide the implementation details of how the cards are
represented. For example, the implementation seen here loads cards from
an SQL database into python data structures, and implements the game
operations on those in-memory structures. An alternative
implementation would have all those operations be implemented as SQL
queries on the database.

Beyond insulation from implementation details, the API is abstract
enough that dialog works on any kind of subject deck, as long as the
cards may be seen as having question and answer properties.

The big payoff, though, is that the code for dialog() is clear and
simple.

Version 1
----------------------------------------
Work though a deck of flashcards. Learned cards are discarded. Missed
cards are saved to a retry deck. When the draw deck is empty, it is
replaced by a shuffled retry deck. The game ends when all the cards
have been learned.

This script is a simplified variant of another flashcard program that
I wrote. Here, the user responses are restricted to just show-card,
save-card and toss-card. In this version the users cannot request that
the deck be restacked nor can they get a progress report. These
restrictions made it simple to code the dialog in block-structured
form, rather than as a state machine.

