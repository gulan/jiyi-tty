#!/usr/bin/env python3

import random
import sqlite3

# There are two classes here. They have the same interface, but
# different internal operations.
#
#   chinese_list: initial load from db, but operate using python lists.
#   SQL: Keep all state in the database. Use transactions to modify the state.
#
# The prototype used chinese_list. The production version needs to use SQL.

class chinese_list(object):
    """Operations on a flashcard deck"""

    @property
    def question(self):
        """Return a formatted question string derived from the card on
        to of the draw deck. The proper formatting depends on the
        subject. The formatting for Chinese vocabulary will
        differ from multiplication tables."""
        (chinese,pinyin,_) = self.deck[-1]
        return [chinese,pinyin]
        
    @property
    def answer(self):
        """Return a formatted answer string."""
        (_,_,english) = self.deck[-1]
        return [english]

    def toss(self):
        """Remove the card from the game. This operation is also known
        as discard. For testing purposes only, the removed cards are
        kept in the trash."""
        card = self.deck.pop()
        self.trash.add(card)
    
    def keep(self):
        """Save the card to the retry deck. The user may put these
        cards back into play with the restack()."""
        card = self.deck.pop()
        self.retry.append(card)

    def restack(self):
        """Shuffle and stack any kept cards to top of the play deck."""
        # Make sure that the recently played cards are placed at the
        # end of the new deck.
        n = len(self.retry) // 2
        r1,r2 = self.retry[:n],self.retry[n:]
        random.shuffle(r1)
        random.shuffle(r2)
        self.deck,self.retry = r2+r1,[]
        # r1,r2 are flipped cards are drawn from the end of the list.

    @property
    def more(self):
        """True if there are more cards in the draw deck."""
        return len(self.deck) > 0
        
    @property
    def gameover(self):
        """True if both the draw deck and save deck are empty."""
        return len(self.deck) == 0 and len(self.retry) == 0 
        
    def check_endgame(self):
        assert set(self.cards) == self.trash

    def _load(self,dbpath,card_count):
        """Create game state."""
        q = """          
        select distinct chinese,pinyin,english
        from hsk
        where rank_id = 1
        order by random()
        limit ?;"""
        cx = sqlite3.connect(dbpath)
        cur = cx.cursor()
        r = cur.execute(q,(card_count,))
        self.cards = list(r)   # the original deck is not really needed.
        self.deck = self.cards[:]
        self.retry = []
        self.trash = set()

    def __init__(self,card_count=30):
        self._load('hsk2009.db',card_count)

class SQL(object):
    """Operations on a flashcard deck"""
    
    @property
    def question(self):
        (_,chinese,pinyin,english) = self._topcard()
        return [chinese,pinyin]

    @property
    def answer(self):
        (_,chinese,pinyin,english) = self._topcard()
        return [english]

    def toss(self):
        """Remove the card from the game. This operation is also known
        as discard. For testing purposes only, the removed cards are
        kept in the trash."""
        cur = self.cx.cursor()
        r = cur.execute('select * from deck limit 1;')
        card = next(r)[0]
        cur.execute('insert into trash values (?);', (card,))
        cur.execute('delete from deck where save_id = ?;', (card,))
    
    def keep(self):
        """Save the card to the retry deck. The user may put these
        cards back into play with the redo()."""
        cur = self.cx.cursor()
        r = cur.execute('select * from deck limit 1;')
        card = next(r)[0]
        cur.execute('insert into save values (?);', (card,))
        cur.execute('delete from deck where save_id = ?;', (card,))
        
    def restack(self):
        """Shuffle and stack any saved cards on top of the play deck."""
        # TBD: recently seen cards should come last
        q = """
        alter table deck rename to deck0;
        create table deck as 
            select * from (select * from save order by random())
            union all
            select * from deck0;
        delete from save;
        drop table deck0;
        """
        cur = self.cx.cursor()
        cur.executescript(q)

    # select * from hsk order by random() limit (select count(*)/1000 from hsk);
        
    @property
    def more(self):
        cur = self.cx.cursor()
        count = next(cur.execute('select count(*) from deck;'))[0]
        return count > 0
        
    @property
    def gameover(self):
        if self.more:
            return False
        cur = self.cx.cursor()
        count = next(cur.execute('select count(*) from save;'))[0]
        return count == 0
        
    def check_endgame(self):
        assert True, "tbd"

    # def _load(self,dbpath,card_count):
    #     q1 = """
    #     drop table if exists deck;
    #     drop table if exists save;
    #     drop table if exists trash;
        
    #     create table deck (deck_id references hsk);
    #     create table save (save_id references hsk);
    #     create table trash (trash_id references hsk);
    #     """
    #     q2 = """
    #     insert into save 
    #       select hsk_id 
    #       from hsk
    #       where rank_id = ?
    #       order by random()
    #       limit ?;
    #     """
    #     self.dbpath = dbpath
    #     self.cx = sqlite3.connect(dbpath)
    #     cur = self.cx.cursor()
    #     cur.executescript(q1)
    #     cur.execute(q2,(2,card_count))
    #     self.restack()

    def __init__(self,card_count=30,dbpath='hsk2009.db'):
        # self._load('hsk2009.db',card_count)
        q1 = """
        drop table if exists deck;
        drop table if exists save;
        drop table if exists trash;
        
        create table deck (deck_id references hsk);
        create table save (save_id references hsk);
        create table trash (trash_id references hsk);
        """
        
        q2 = """
        insert into save 
          select hsk_id 
          from hsk
          where rank_id = ?
          order by random()
          limit ?;
        """
        
        self.dbpath = dbpath
        self.cx = sqlite3.connect(dbpath)
        cur = self.cx.cursor()
        cur.executescript(q1)
        cur.execute(q2,(2,card_count))
        self.restack()

    def _topcard(self):
        q0 = "select save_id from deck limit 1;"
        q1 = """select hsk_id,chinese,pinyin,english
                from hsk 
                where hsk_id = ?;"""
        cur = self.cx.cursor()
        card_id = next(cur.execute(q0))[0]
        card = next(cur.execute(q1,(card_id,)))
        assert card_id == card[0]
        return card
        
