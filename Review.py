from Sentence import Sentence
from Database import Database
from apyori import apriori # We use apriori to extract frequent feature from feature list
from Feature import Feature

class Review:
	# First config for read
	column = ['sentences'] # column
	table_name = 'sentences' # table name

	'''
		This class provide interface to extract the feature and get the opinion text. This is our main process
	'''
	def __init__(self, file_name, id_anime, judul_anime, feature = []) :
		self.feature_list = set(feature) # Our feature list
		self.noun_list = [] # Our noun list use for transaction and mining the frequent feature
		self.id_anime = id_anime

		self.db = Database(file_name) # Our databse interface
		data = self.db.read(self.table_name, self.column, ' WHERE anime_id='+id_anime)
		self.judul_anime = judul_anime
		self.sentences = []

		# The review is consist a sentence class
		# You can look at the sentence class to see what can a sentence do include post tagging, tokenizing and so on
		for row in data:
			self.sentences.append(Sentence(row[0].lower(), 5114))
		self.feature_result = []

	'''
		This method provide an interface to extract the feature list. The process is like this

		- Use the post tagging to find the noun or a feature candidate.
		- Save to the noun list
		- Use assosiation mining to find the frequent feature
		- Save to the feature list
	'''
	def extract_feature_list(self):

		if len(self.feature_list) == 0:
			# Get the noun for each sentences
			for sentence in self.sentences:

				for word in sentence.tagged :
					if word[1] == 'NN' :
						sentence.noun.append(word[0])

				# If the sentences didn't countain noun, it's just a dump sentences
				if len(sentence.noun) > 0 :
					sentence.opinion = True
					self.noun_list.append(sentence.noun)
				else :
					sentence.opinion = False


			# Use apriori method to mine the feature
			association_rules = apriori(self.noun_list, min_support=0.001, min_confidence=0, min_lift=3, min_length=2)
			association_results = list(association_rules)

			features = []

			for item in association_results:
				pair = item[0] 
				items = [x for x in pair]
				self.feature_list.add(items[0])

	'''
		After mine the feature list we mine the opinion about that feature.

		- First, we get the adjective that most nearby to the noun
		- We categorize them with positive or negative with wordnet
	'''
	def extract_feature_opinion(self):

		# List all the feature and make them the key to the dictionary
		feature_count = {}
		for feature in self.feature_list :
			feature_count[feature] = []

		# Find all feature and opinion in all sentences
		for sentence in self.sentences:

			if sentence.opinion == True:
				all_words = len(sentence.tagged)
				for i,j in enumerate(sentence.tagged) :

					# Find the nearby adjective forward or backward
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

		# Make the feature class that contain the feature count of positive opinion and negative opinion
		for i in feature_count.keys():
			self.feature_result.append(Feature(self.db, i, feature_count[i], self.id_anime))

		# Use wordnet to mine the opinion orientation
		Feature.OrientationPrediction(Feature.all_adj, Feature.seed)
		# print(Feature.seed)

	def get_summary(self):
		self.extract_feature_list()
		self.extract_feature_opinion()
		for i in self.feature_result:
			i.view()

	# Save method
	def save(self) :
		for feature in self.feature_result:
			feature.save()

	# Close database
	def close_db(self):
		self.db.close()