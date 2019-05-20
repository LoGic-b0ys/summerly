import nltk
from nltk.corpus import stopwords
import sqlite3

conn = sqlite3.connect('review_anime.db')

stop_word = set(stopwords.words("english"))

sentences = []

cursor = conn.execute("SELECT sentences from sentences")
for row in cursor:
	sentences.append(row[0].lower())

sql = ''' INSERT INTO sentence_noun(noun_list) VALUES(?) '''
cur = conn.cursor()

for sentence in sentences :
	words = nltk.word_tokenize(sentence)
	filtered = []

	for word in words :
		if word not in stop_word :
			filtered.append(word)

	tagged = nltk.pos_tag(filtered)

	nouns = ''
	for word in tagged :
		if word[1] == 'NN' :
			nouns += word[0] + ','
	# print((nouns))
	cur.execute(sql, (nouns, ))

conn.commit()
conn.close()