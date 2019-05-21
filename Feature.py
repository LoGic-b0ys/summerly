import nltk
from nltk.corpus import wordnet
from Database import Database

class Feature :
	table_name = 'opinion_orientation'
	column = ['id_anime','feature_name','good', 'bad']
	seed = {'top':1,'unpredictable':1,'large':1,'admirable':1,'addictive':1, 'nice':1, 'funny':1, 'boring': -1}
	all_adj = set()

	def __init__(self, conn, feature, adj_list, id_anime):
		self.feature = feature
		self.conn = conn
		self.adj_list = adj_list
		self.good = 0
		self.bad = 0
		for i in adj_list:
			Feature.all_adj.add(i.lower())
		self.id_anime = id_anime

	def count(self):
		for i in self.adj_list:
			if i in Feature.seed :
				if Feature.seed[i] == 1 :
					self.good += 1
				else :
					self.bad += 1

	def save(self):
		self.count()
		data = (self.id_anime, self.feature, self.good, self.bad)
		self.conn.insert(self.table_name, self.column, data)
		self.conn.commit()

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
			Feature.OrientationSearch(adj_list, seed_list)
			s2 = len(seed_list)

			if s1 == s2 :
				break

# # First config for read
# column = ['feature', 'opinion'] # column
# table_name = 'feature_opinion' # table name

# # Get data from database
# db = Database('review_anime.db')
# data = db.read(table_name, column)

# # Preprocess the data
# opinions = {}
# opinion_list = set()
# opinion_count = []

# # Preprocess the data
# for row in data:
# 	curr_opinion = row[1].split('|')[:-1]
# 	opinions[row[0]] = curr_opinion
# 	for words in curr_opinion :
# 		opinion_list.add(words.lower())

# for key in opinions.keys():
# 	res = [0,0]
# 	for word in opinions[key]:
# 		if word in seed:
# 			if seed[word] == 1:
# 				res[0] += 1
# 			else :
# 				res[1] += 1
# 	# opinion_count[key] = res
# 	current = Feature(db, key, res[0], res[1], 5114)
# 	opinion_count.append(current)

# for feature in opinion_count :
# 	feature.save()

# # db.commit()
# db.close()