import nltk
from nltk.corpus import wordnet
from Database import Database

'''
	This class provide the feature. Main goal of this class is to determine the oopinion orientation, count the opinion
'''
class Feature :
	table_name = 'opinion_orientation'
	column = ['id_anime','feature_name','good', 'bad']

	# This seed is used to determine the orientation
	# Atfter several operation this seed will grow with help of wordnet
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

	'''
		This method provide an interface to count the positive and negative event
	'''
	def count(self):
		for i in self.adj_list:
			if i in Feature.seed :
				if Feature.seed[i] == 1 :
					self.good += 1
				else :
					self.bad += 1

	def view(self):
		self.count()
		print('Feature: '+self.feature)
		# for i in self.adj_list[:-1] :
		# 	print(i + ',', end='')
		# print(self.adj_list[-1])

		print('Good: ' + str(self.good))
		print('Bad: ' + str(self.bad))

	def save(self):
		self.count()
		data = (self.id_anime, self.feature, self.good, self.bad)
		self.conn.insert(self.table_name, self.column, data)
		self.conn.commit()

	'''
		This method provide an interface to scan all the adjective list and compare it with the seed.
		If it has synonim or antonym to the seed then we can conclude the orientation and vice versa
	'''
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

	'''
		We will scan through the list until we can't find a related word
	'''
	def OrientationPrediction(adj_list, seed_list):
		while True:
			s1 = len(seed_list)
			Feature.OrientationSearch(adj_list, seed_list)
			s2 = len(seed_list)

			if s1 == s2 :
				break