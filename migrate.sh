#! /bin/sh

path=`gdg backup`
mv hsk2009.db $path
cp hsk2009.sql $path
sqlite3 <hsk2009.sql hsk2009.db

