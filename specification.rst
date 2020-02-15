Definitions
----------------------------------------
These definitions can be skipped on first reading. I find that keeping
a dictionary of terms guards against introducing synonyms in the
prose. Having more than one name for any concept is confusing.

[I need to update this vocabulary as the code no longer uses many of
these terms.]

Game
  Flash card sessions are not usually called games, but what
  definition of 'game' would include Solitaire and exclude flash cards?

Player
  the user of our game during the course of play.

Card
  A card is a pair of (question, answer). The representation of
  these fields can remain unspecified until concrete implementations
  are considered. A card in the dealt deck also needs an
  orientation. (question, answer, answer-up). Answer-up is a Boolean
  with the obvious meaning. The question/answer pair uniquely
  identifies a card. A game has no duplicate cards.

Card Set
  The set of all cards used for any play of the game. The card
  set is fixed during play, but of course the player can choose any set
  at the start of a game.

Deck
  During the course of play, the card set is partitioned into
  four decks: dealt, play, kept and trash. Any of these decks may be
  empty. Cards move among the decks during the course play, but the
  union of all of the decks is always equal to the card set.

Dealt Deck
  The currently dealt card. It may appear as answer-up or
  answer down. This deck never has more than one card, but it may be
  empty. Note that I usually say the "the dealt card" rather than "the
  top card of the dealt deck." The later is not wrong, but it is
  misleading, as there is no other card in the deck.

Trash Deck
  Cards that have been learned are tossed in the trash. The
  trash cards are never used again during the course of play. They are
  of no use to the program, but an explicit trash deck makes stating the game
  invariant easier. The trash deck is represented as a set.

Play Deck
  The source of cards to learn. Initially the entire card set
  appears in the play deck. Each deal operation moves the top card to
  the dealt deck. The shuffle operation moves all the cards from the
  kept deck to the top of the play deck. The play deck is a list of
  cards. There is no defined ordering relation on cards.

Kept Deck
  Cards that have been played, but not declared learned are
  saveed to the kept deck. Kept card are put back in play by the shuffle
  operation. The kept deck is a sequence with the most recent cards
  going to the end. The arrangement allows me to prevent recently seen
  cards from being immediately dealt again after a shuffle.

(Game) State
  The four decks: (dealt, play, kept and trash) plus the
  card set comprise the state. The card set never changes in any game
  play. The obvious optimization is to leave the card set out of the
  state, but I need it to specify the game invariant.

Start State
  At the beginning of a game play, the card set is shuffled
  in the the play deck. This is the result of the init operation.

Operation
  An operation changes the game state. Formally, the operation
  is a triple (before-state, operation-name, after-state). The set of
  operations are predefined and unchanging. We often refer to the
  operation by its name. We can also talk about the operation-triple.

Init (Operation)
  Establishes the start state.

Deal (Operation)
  Move the top card of the play deck to the dealt
  deck, question side up.

Flip (Operation)
  Turn over the dealt card to reveal the answer.

Keep (Operation)
  Move the dealt card to the kept deck

Toss (Operation)
  Move the dealt card to the trash deck

Shuffle (Operation)
  Randomize the kept deck, and place it on top of
  the play deck (which might be empty)

Introduction
----------------------------------------
The goal of a user (henceforth the "player") is to learn a set of
facts, say a Chinese vocabulary, or maybe the prime factors of the
first 100 integers. This system presents a flash card game to assist
the player in achieving this goal.

Informally, the player does the following::

    start game with a card set
    while there are more unlearned cards:
        see question on the dealt card
        say answer out loud
        flip card
        self-score answer

There are two parts of the design to consider:

* The game state and operations on the state
* The user interface

I start with the first.

State Operations
----------------------------------------
The state is a five-tuple (card-set, dealt, play, kept, trash). The
card-set, dealt deck and trash are sets of cards as the sequence of
the cards do not matter.

The play deck is a stack of cards. The order is random, but must be
preserved. Cards are drawn from the top, and shuffled cards are added
to the top in bulk.

The kept deck is a list of cards. Each kept card are appended to the
end of the list. The shuffle operation resets the kept deck to the
empty list.

The dealt deck is a set containing at most one card. The card is
represented by a triple (question, answer, answer-up).

The cards in the other desks are represented by pairs (question,
answer). These two fields identify the card by value.

A system invariant is card set is equal to the union of the four decks
(assuming that answer-up flag in ignored when comparing cards.) Keep
this invariant in mind, and we need not again refer the card-set.

My ad hoc specification language is a hybrid of something like Z/TLA+
and Python. The prime designates the after state of a variable. For
example, x' = x, means that x was not changed. (y == 0, y' == y + 1,
y' == 1) is true. Remember that each line is a predicate and the lines
are joined by conjunction. Python expressions are used only if they have
no side-effects. The assignment statement is forbidden.

Init
----------------------------------------

::

    dealt' == {}
    play' == rand(card-set)
    kept' == []
    trash' == {}

GameOver
----------------------------------------

::

    dealt == {}
    play == []
    kept == []
    trash == card-set

Deal
----------------------------------------

::

    dealt == {}
    len(play) > 0
    (answer, question) == play[0]
    dealt' == {(answer, question, True)}
    play' == play[1:]
    kept' == kept
    trash' == trash

Flip
----------------------------------------
Only the dealt card changes it state from answer-up == true to
answer-up == false. The identity of the dealt card remains the same. The
number of dealt card remains 1. The other stacks are not changed.

::

    dealt == {(question, answer, True)}
    dealt' == {(question, answer, False)}
    play' == play
    kept' == kept
    trash' == trash

Keep
----------------------------------------

::

    {(question, answer, False)} == dealt
    dealt' == {}
    play' == play
    kept' == kept + [(question, answer)]
    trash' == trash 

Toss
----------------------------------------

::

    {(question, answer, False)} == dealt
    dealt' == {}
    play' == play
    kept' == kept
    trash' == trash `union` {(question, answer)}

Shuffle
----------------------------------------

::

    dealt == {}
    dealt' == dealt
    play' == rand(kept) ++ play
    kept' == []
    trash' == trash

The function rand() is what performs the actual shuffle. I could
assume that it is a built-in operation that I need not specify. But
there are a couple of problems. The shuffle should not be purely
random. It should place recently seen cards at the end of the shuffled
sequence.

::

    play' == rand(first-half(kept)) ++ rand(second-half(kept)) ++ play

Also, while this is not difficult in Python, doing the same in SQL is
more of a challenge.

