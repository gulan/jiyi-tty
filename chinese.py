#!/usr/bin/env python3

import random
import sqlite3

class SQL(object):
    
    """ Operations on a flashcard deck """
    
    @property
    def question(self):
        (chinese,pinyin,english,live) = self._topcard()
        if live == 1:
            return [chinese]
        if live == 2: # easy
            return [chinese,pinyin]

    @property
    def answer(self):
        (chinese,pinyin,english,live) = self._topcard()
        if live == 1:
            return [pinyin, english]
        if live == 2:
            return [english]
        
    def _topcard(self):
        # make single query
        cur = self.cx.cursor()
        
        q0 = "select save_id,live from deck limit 1;"
        (card_id,live) = next(cur.execute(q0))[0:2]

        q1 = """select chinese, pinyin, english
                from hsk 
                where hsk_id = ?;"""
        card = (chinese,pinyin,english) = next(cur.execute(q1,(card_id,)))
        return card + (live,)

    def toss(self):
        """Remove the card from the game. This operation is also known
        as discard. For testing purposes only, the removed cards are
        kept in the trash."""
        cur = self.cx.cursor()
        r = cur.execute('select * from deck limit 1;')
        (key,live) = next(r)[0:2]
        live -= 1
        if live == 0:
            cur.execute('insert into trash values (?);', (key,))
        else:
            cur.execute('insert into save values (?,?);', (key,live))
        cur.execute('delete from deck where save_id = ?;', (key,))
        self.cx.commit()
    
    def keep(self):
        """Save the card to the retry deck. The user may put these
        cards back into play with the redo()."""
        cur = self.cx.cursor()
        r = cur.execute('select * from deck limit 1;')
        (key, live) = next(r)[0:2]
        cur.execute('insert into save values (?,?);', (key,live))
        cur.execute('delete from deck where save_id = ?;', (key,))
        self.cx.commit()
        
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
        self.cx.commit()

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
        
    def __init__(self,card_count=30,dbpath='hsk2009.db'):
        q1 = """
        delete from deck;
        delete from save;
        delete from trash;
        """
        
        q2 = """
        insert into save 
          select hsk_id,2
          from hsk
          where rank_id = ?
          order by random()
          limit ?;
        """
        
        q3 = """
          insert into game (tm, ccnt)
          values (datetime('now'), ?);
        """
        
        self.dbpath = dbpath
        self.cx = sqlite3.connect(dbpath)
        cur = self.cx.cursor()
        cur.executescript(q1)
        cur.execute(q3,(card_count,))
        cur.execute(q2,(2,card_count))
        self.cx.commit()
        self.restack()

    def _list_saved(self):
        # not for use, just remember how to join with foreign key:
        q = """select * from saved,hsk where save_id = hsk.rowid;"""
        cur = self.cx.cursor()
        for row in cur.execute(q):
            print(row)

    @property
    def progress(self):
        """
        provide "learned/count" string
        """
        q = """
            select ccnt from game 
            where game_id = (select max(game_id) from game);
            """
        cur = self.cx.cursor()
        count   = next(cur.execute(q))[0]
        unseen  = next(cur.execute("select count(*) from deck;"))[0]
        missed  = next(cur.execute("select count(*) from save;"))[0]
        ## learned = next(cur.execute("select count(*) from trash;"))[0]
        ## assert count == unseen + missed + learned
        learned = count - unseen - missed
        return "%s/%s" % (learned, count)
