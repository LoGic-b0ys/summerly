from Sentence import Sentence
from Database import Database
from apyori import apriori
from Feature import Feature

class Review:
	# First config for read
	column = ['sentences'] # column
	table_name = 'sentences' # table name

	def __init__(self, file_name, id_anime, judul_anime) :
		self.feature_list = set() # List kata dalam feature
		self.noun_list = [] # List noun for transaction
		self.id_anime = id_anime
		self.db = Database(file_name)
		data = self.db.read(self.table_name, self.column, ' WHERE anime_id='+id_anime)
		self.judul_anime = judul_anime
		self.sentences = []
		for row in data:
			self.sentences.append(Sentence(row[0].lower(), 5114))
		print(len(data))
		self.feature_result = []

	def extract_feature_list(self):
		for sentence in self.sentences:
			for word in sentence.tagged :
				if word[1] == 'NN' :
					sentence.noun.append(word[0])
			if len(sentence.noun) > 0 :
				sentence.opinion = True
				self.noun_list.append(sentence.noun)
			else :
				sentence.opinion = False

		association_rules = apriori(self.noun_list, min_support=0.001, min_confidence=0, min_lift=3, min_length=2)
		association_results = list(association_rules)

		features = []

		for item in association_results:
			pair = item[0] 
			items = [x for x in pair]
			self.feature_list.add(items[0])

	def extract_feature_opinion(self):
		feature_count = {}
		for feature in self.feature_list :
			feature_count[feature] = []

		for sentence in self.sentences:

			if sentence.opinion == True:
				all_words = len(sentence.tagged)
				for i,j in enumerate(sentence.tagged) :
					if j[1] == 'NN' and j[0] in self.feature_list :
						count_forward = i
						count_backward = i
						while count_forward < all_words and sentence.tagged[count_forward][1] != 'JJ' :
							count_forward += 1
						while count_backward >= 0 and sentence.tagged[count_backward][1] != 'JJ' :
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
							feature_count[j[0]].append(sentence.tagged[count][0])

		for i in feature_count.keys():
			self.feature_result.append(Feature(self.db, i, feature_count[i], self.id_anime))

		Feature.OrientationPrediction(Feature.all_adj, Feature.seed)

	def save(self) :
		for feature in self.feature_result:
			feature.save()

	def close_db(self):
		self.db.close()