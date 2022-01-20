select 
	w.word, 
	w.stem, 
	l.usage, 
	l.timestamp,
	b.title,
	datetime(l.timestamp/1000.0, 'unixepoch') as lookup_timestamp
from lookups l
	join words w on w.id = l.word_key
	join dict_info d on d.id = l.dict_key
	join book_info b on b.id = l.book_key
where w.lang='ja'
	and d.langin = 'ja'
	and d.langout = 'ja'
	{time_filter}
order by l.timestamp desc