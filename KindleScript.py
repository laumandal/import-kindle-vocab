# coding: utf-8

import sys
import sqlite3
import os
import pandas as pd
import datetime

vocabdb = "/Volumes/Kindle/system/vocabulary/vocab.db"
#vocabdb = "vocab3.db"

if not os.path.isfile(vocabdb):
    print ("Could not find vocab database.")
else:
    #construct sql query
    sql_query = """
    SELECT usage, stem, word, langin, langout
    FROM LOOKUPS
    JOIN WORDS 
    ON LOOKUPS.word_key = WORDS.id
    JOIN DICT_INFO
    ON DICT_INFO.asin = LOOKUPS.dict_key;
    """

    conn=sqlite3.connect(vocabdb)
    #create DataFrame by running query
    data = pd.read_sql(sql_query,conn)
    conn.close()

    def replace_pairs(string, pairs):
        for p0, p1 in pairs:
            string = string.replace(p0,p1) 
        return string

    def replace_dotdash(string):
        return replace_pairs(string,[('・',""),('‐',"")])

    data['stem'] = [replace_dotdash(stem) for stem in data.stem]


    def tag_word(full_string,string_to_tag,tag1,tag2):
        return full_string.replace(string_to_tag,"{0}{1}{2}".format(tag1,string_to_tag,tag2))

    def bolden_word(full_string,string_to_bold):
        return tag_word(full_string,string_to_bold,"<b>","</b>")

    def format_usage(full_string,study_word):
        if study_word in full_string:
            return bolden_word(full_string,study_word)
        else:
            return "{0} (study word:{1})".format(full_string,study_word)
        
    data.usage = [format_usage(usage, word) for (usage, word) in zip(data.usage, data.word)]

    data['tags'] = "日本語 kindle"
    data['stem'] =  data['stem'] + ": "

    timestamp = datetime.datetime.now()
    #reverse the order to make from newest card. quicker than importing timestamp and sorting then dropping column
    vocabfilename = timestamp.strftime('KindleVocab_%Y%b%d_%H%M.csv')
    data[::-1].to_csv(vocabfilename,header=False,index=False,encoding='utf-8')

    #clear db on kindle
    conn=sqlite3.connect(vocabdb)
    c = conn.cursor()
    c.execute("""DELETE FROM WORDS;""")
    c.execute("""DELETE FROM LOOKUPS;""")
    conn.commit()
    conn.close()

    print ("Vocab file " + vocabfilename +" created.")
