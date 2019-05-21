import nltk
from nltk.corpus import stopwords

class Sentence:
	stop_word = set(stopwords.words("english"))

	def __init__(self, sentence, id_anime):
		words = nltk.word_tokenize(sentence)
		filtered = []

		for word in words :
			if word not in Sentence.stop_word :
				filtered.append(word)

		self.tagged = nltk.pos_tag(filtered)
		self.opinion = True
		self.id_anime = id_anime
		self.noun = []

	def get_nouns(self) :
		return self.noun

	def get_sentence(self) :
		return sentence