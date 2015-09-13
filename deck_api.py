#! /usr/bin/env python

# This module is documentation. I do not use it anywhere.

class API(object):
    """Operations on a flashcard deck"""

    def toss(self):
        """Remove the card from the game. This operation is also known
        as discard. For testing purposes only, the removed cards are
        kept in the trash."""
    
    def keep(self):
        """Save the card to the retry deck. The user may put these
        cards back into play with the redo()."""

    def restack(self):
        """Shuffle and stack any saved cards to top of the play deck."""

    @property
    def more(self):
        """True if more cards in the draw deck."""
        
    @property
    def gameover(self):
        """True if both the draw deck and save deck are empty."""

    @property
    def question(self):
        """Return a formatted question string derived from the card on
        to of the draw deck. The proper formatting depends on the
        subject. The formatting for Chinese vocabulary would likely
        differ from multiplation tables."""

    @property
    def answer(self):
        """Return a formatted answer string."""
        
    def load(self):
        """Create game state."""
