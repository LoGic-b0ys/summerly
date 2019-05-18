import sqlite3
from nltk.tokenize import word_tokenize
import nltk

conn = sqlite3.connect('review_anime.db')

opinions = []
cursor = conn.execute("SELECT opinion_text from opinion_sentence")
for row in cursor:
	opinions.append(row[0])

feature_list = []
cursor = conn.execute("SELECT feature from feature")
for row in cursor:
	feature_list = row[0].split('|')[:-1]

feature_count = {}
for feature in feature_list :
	feature_count[feature] = []

for opinion in opinions :
	words = word_tokenize(opinion)
	tagged = nltk.pos_tag(words)
	all_words = len(tagged)
	for i,j in enumerate(tagged) :
		if j[1] == 'NN' and j[0] in feature_list :
			count_forward = i
			count_backward = i
			while count_forward < all_words and tagged[count_forward][1] != 'JJ' :
				count_forward += 1
			while count_backward >= 0 and tagged[count_backward][1] != 'JJ' :
				count_backward -= 1

			count = -1
			if count_forward < all_words and count_backward >= 0 :
				if(count_forward - i > i - count_backward) :
					count = count_backward
				else :
					count = count_forward

			if count_backward < 0 :
				count = count_forward
			if count_forward >= all_words :
				count = count_backward
			if count_forward >= all_words and count_backward < 0 :
				count = -1

			if count != -1 :
				feature_count[j[0]].append(tagged[count][0])

sql = ''' insert into feature_opinion(id_anime,opinion,feature) values(?,?,?) '''
cnt = conn.cursor()

for feature in feature_count.keys() :
	opinion_text = ''
	for opinion in feature_count[feature] :
		opinion_text += opinion + '|'
	cnt.execute(sql, (5114, opinion_text, feature))

conn.commit()
conn.close()