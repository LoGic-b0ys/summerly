from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import wordnet

from Database import Database

def OrientationSearch(adj_list, seed_list):
	for word in adj_list:
		synonim = []
		antonym = []
		for syn in wordnet.synsets(word):
			for l in syn.lemmas():
				synonim.append(l.name())
				if l.antonyms():
					antonym.append(l.antonyms()[0].name())
		for w in synonim:
			if w in seed_list:
				seed_list[word] = seed_list[w]
				break;
		for w in antonym:
			if w in seed_list:
				seed_list[word] = -1*seed_list[w]
				break;

def OrientationPrediction(adj_list, seed_list):
	while True:
		s1 = len(seed_list)
		OrientationSearch(adj_list, seed_list)
		s2 = len(seed_list)

		if s1 == s2 :
			break

# First config for read
column = ['feature', 'opinion'] # column
table_name = 'feature_opinion' # table name

# Get data from database
db = Database('review_anime.db')
data = db.read(table_name, column)

# Preprocess the data
opinions = {}
opinion_list = set()
opinion_count = {}
seed = {'top':1,'unpredictable':1,'large':1,'admirable':1,'addictive':1, 'nice':1, 'funny':1, 'boring': -1}

# Preprocess the data
for row in data:
	curr_opinion = row[1].split('|')[:-1]
	opinions[row[0]] = curr_opinion
	for words in curr_opinion :
		opinion_list.add(words.lower())

OrientationPrediction(opinion_list, seed)

for key in opinions.keys():
	res = [0,0]
	for word in opinions[key]:
		if word in seed:
			if seed[word] == 1:
				res[0] += 1
			else :
				res[1] += 1
	opinion_count[key] = res

print(opinion_count)

column_out = ['id_anime','feature_name','good', 'bad']
table_name_out = 'opinion_orientation'
for opinion in opinion_count.keys() :
	data = (5114, opinion, opinion_count[opinion][0], opinion_count[opinion][1])
	db.insert(table_name_out, column_out, data)

db.commit()
db.close()