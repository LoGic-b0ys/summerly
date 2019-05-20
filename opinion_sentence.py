import sqlite3
from nltk.tokenize import word_tokenize

conn = sqlite3.connect('review_anime.db')

sentences = []
cursor = conn.execute("SELECT sentences from sentences")
for row in cursor:
	sentences.append(row[0])

features = []
cursor = conn.execute("SELECT feature from feature")
for row in cursor:
	features.append(row[0])

# print(sentences)
features_list = features[0].split('|')[:-1]
opinion_sentence = []

for sentence in sentences :
	sentence_word = word_tokenize(sentence)
	if any(x in features_list for x in sentence_word):
		opinion_sentence.append(sentence)

sql = ''' insert into opinion_sentence(id_anime,opinion_text) values(?,?) '''
cnt = conn.cursor()

for opinion in opinion_sentence :
	cnt.execute(sql, (5114, opinion))

conn.commit()
conn.close()